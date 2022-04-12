from functools import total_ordering
from itertools import product
import pymysql
from flask_apispec import MethodResource, marshal_with, doc, use_kwargs
import util
from flask_jwt_extended import create_access_token, jwt_required
from datetime import timedelta
import user_swagger_model #.是同一層資料夾的東西
import json

#db_connected
def db_init():
    db = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='root',
        port=3307,
        db='cart'
    )
    cursor = db.cursor(pymysql.cursors.DictCursor)
    return db, cursor

    
####### API Action #########

class Cart(MethodResource): 

    # 查詢購物車內容，並可顯示倉庫可購買的商品清單
    @doc(description='購物車清單', tags=['購物車'])
    @use_kwargs(user_swagger_model.UserGetSchema,location='query') 
    @marshal_with(user_swagger_model.UserGetResponse, code=200)
    def get(self,**kwargs):
        db, cursor = db_init()
        name = kwargs.get("name") 
        if name is not None:
            sql = f"SELECT * FROM cart.buy WHERE name = '{name}';"
        else:
            sql = 'SELECT * FROM cart.buy;'
            print(sql)
        cursor.execute(sql)
        users = cursor.fetchall()
        db.close()
        return util.success(users)
        

    # 新增商品，會分辨是否會買得比倉庫多，從倉庫查找價格，並計算總金額
    @doc(description='新增商品.', tags=['購物車'])
    @use_kwargs(user_swagger_model.UserPostSchema,location='form')
    @marshal_with(user_swagger_model.UserPostResponse, code=200)
    def post(self,**kwargs):
        db, cursor = db_init()
        user = {
            'name': kwargs['name'],
            'number': kwargs['number'],
        }
        sql=f"SELECT * FROM `cart`.`warehouse` WHERE name = '{user['name']}';" #取倉庫該商品的資料
        cursor.execute(sql)
        product=cursor.fetchall()
        #確認庫存>購買數量
        if int(product[0]['quantity']) < int(user['number']): 
            return {'message':'倉庫庫存不足'}
        else:
            totalcost=product[0]['price']*int(user['number'])#計算該品項購買的總金額
            user.update({'cost':totalcost})
            #更新庫存
            sql=f"""
            UPDATE cart.warehouse
            SET quantity ='{int(product[0]['quantity'])-int(user['number'])}'
            WHERE name ='{user['name']}'

            """
            cursor.execute(sql)
            #將購買商品放入購物車
            sql = """
            INSERT INTO `cart`.`buy` (`name`,`number`,`cost`)
            VALUES ('{}','{}','{}');

            """.format(user['name'], user['number'], totalcost)
            cursor.execute(sql)
            users = cursor.fetchall()
            db.commit()
            db.close()
            return util.success(user)


    #修改購買的商品數量，並會協助重新計算價格
    @doc(description='修改購物車', tags=['購物車'])
    @use_kwargs(user_swagger_model.UserPatchSchema,location='query') #呼叫過來使用,get的話location都是query
    @marshal_with(user_swagger_model.UserCommonResponse, code=201)#marshal_with的內容會出現在Response
    def patch(self, **kwargs):
        db, cursor = db_init()
        new_name= kwargs.get('name') #要修改的名子
        number= kwargs.get('number')#修改後的數量
        sql=f"SELECT * FROM cart.buy WHERE name = '{new_name}';"
        cursor.execute(sql)
        old_product_data=cursor.fetchall() 
        sql=f"SELECT * FROM cart.warehouse WHERE name = '{new_name}';"
        cursor.execute(sql)
        old_warehouse_data=cursor.fetchall()
        #判斷修改後的數量是否>庫存
        total_quantity=int(old_warehouse_data[0]['quantity'])+int(old_product_data[0]['number'])
        if int(number) > total_quantity:
            return {'通知':'庫存量不足'}
        else:
            #更新庫存
            new_quantity=int(old_warehouse_data[0]['quantity']) + int(old_product_data[0]['number'] - int(number))
            sql=f"""UPDATE cart.warehouse
            SET quantity ='{new_quantity}'
            WHERE name ='{new_name}';
            """
            cursor.execute(sql)
            #更新購物車
            new_cost=int(old_warehouse_data[0]['price'])*int(number)
            sql = f"""UPDATE cart.buy
                SET number = {number},cost ={new_cost}
                WHERE name = '{new_name}';
            """
            print(sql)
            result = cursor.execute(sql)
            db.commit()
            db.close()
            if result == 0:
                return util.failure({"message": "error"})
            return util.success() 

    #刪除購物車品項
    @doc(description='刪除項目', tags=['購物車'])
    @use_kwargs(user_swagger_model.UserDeleteScheam,location='query')
    @marshal_with(user_swagger_model.UserCommonResponse, code=204)
    def delete(self, **kwargs):
        db, cursor = db_init()
        name=kwargs.get('name')
        #抓出庫存數量與原先購物車數量
        sql=f"SELECT * FROM cart.buy WHERE name = '{name}';"
        cursor.execute(sql)
        old_product_data=cursor.fetchall()
        sql=f"SELECT * FROM cart.warehouse WHERE name = '{name}';"
        cursor.execute(sql)
        old_warehouse_data=cursor.fetchall() 
        #更新庫存
        sql=f"""UPDATE cart.warehouse
        SET quantity= '{int(old_product_data[0]['number'])+int(old_warehouse_data[0]['quantity'])}'
        WHERE name ='{name}';
        """
        cursor.execute(sql)
        #刪除購物車
        sql = f"DELETE FROM `cart`.`buy` WHERE name = '{name}';"
        result = cursor.execute(sql)
        db.commit()
        db.close()
        return {'message':'success'}


#結帳
class checkout(MethodResource):
    #要有購買總內容、總金額、帳號、密碼
    @doc(description='結帳', tags=['會員結帳'])
    @use_kwargs(user_swagger_model.LoginSchema, location="form")
    @marshal_with(user_swagger_model.checkoutResponse, code=204)
    def post(self, **kwargs):
        db, cursor = db_init()
        account=kwargs.get('account')
        password=kwargs.get('password')

        sql = f"SELECT * FROM cart.checkout WHERE account = '{account}' AND password = '{password}';"
        cursor.execute(sql)
        print(type(account))
        users = cursor.fetchall()
        if users != ():
            #撈取購物車所有資料
            sql=f"SELECT * FROM cart.buy WHERE 1"
            cursor.execute(sql)
            list=cursor.fetchall()
            product,number,total_cost=[],[],[]
            for i in list:
                product.append(i['name'])
                number.append(i['number'])
                total_cost.append(i['cost'])
            total_cost=sum(total_cost)
            product=dict(zip(product,number))
            product=json.dumps(product)
            #放入結帳資訊
            print('_____')
            print(product)
            print(total_cost)
   
            sql=f"""
            UPDATE cart.checkout
            SET buying_list = '{product}', total_cost= {total_cost}
            WHERE account ='{account}' AND password = '{password}';
            """ #product加''(在mysql中要加，這邊就要加)，不然我們會認為你不是字串辣
            cursor.execute(sql)
            bill=cursor.fetchall()
            print(bill)

            #清空購物車
            sql="TRUNCATE TABLE cart.buy;"
            cursor.execute(sql)
            db.commit()
            db.close()
            return (f'{account}您好，你的購物清單為{product}，總金額是{total_cost}元(請立即結帳，購物車已清空)')
        else:
            return {'通知':'帳號錯誤'}


class signin(MethodResource):
    @doc(description='建立帳號', tags=['創立帳號'])
    @use_kwargs(user_swagger_model.LoginSchema, location="form")
    #@marshal_with(UserLoginResponse, code=200)
    def post(self, **kwargs):
        db, cursor = db_init()
        account = kwargs.get("account") 
        password=kwargs.get('password')
        sql = """
            INSERT INTO cart.checkout (`account`,`password`,`buying_list`,`total_cost`)
            VALUES ('{}','{}','','');
            """.format(account,password)
        cursor.execute(sql)
        p=cursor.fetchall()
        print('你好')
        print(p)
        db.commit()
        db.close()
        return (f'帳號建立成功,您的帳號是{account} 密碼是{password}')

