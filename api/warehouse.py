import pymysql
from flask_apispec import MethodResource, marshal_with, doc, use_kwargs
import util

import warehouse_model
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

class warehouse(MethodResource): 
    # 倉庫清單
    @doc(description='倉庫清單', tags=['倉庫'])
    @use_kwargs(warehouse_model.UserGetSchema,location='query') 
    @marshal_with(warehouse_model.UserGetResponse, code=200)
    def get(self,**kwargs):
        db, cursor = db_init()
        name = kwargs.get("name") 
        if name is not None:
            sql = f"SELECT * FROM cart.warehouse WHERE name = '{name}';"
        else:
            sql = 'SELECT * FROM cart.warehouse;'
            print(sql)
        cursor.execute(sql)
        users = cursor.fetchall()
        db.close()
        return util.success(users)
        

    # 新增倉庫商品,要有名稱、數量、金額
    @doc(description='新增倉庫商品.', tags=['倉庫'])
    @use_kwargs(warehouse_model.UserPostSchema,location='form')
    @marshal_with(warehouse_model.UserPostResponse, code=200)
    def post(self,**kwargs):
        db, cursor = db_init()
        user = {
            'name': kwargs['name'],
            'quantity': kwargs['quantity'],
            'price':kwargs['price']
        }
        sql = """
        INSERT INTO `cart`.`warehouse` (`name`,`quantity`,`price`)
        VALUES ('{}','{}','{}');

        """.format(user['name'], user['quantity'], user['price'])
        cursor.execute(sql)
        users = cursor.fetchall()
        db.commit()
        db.close()
        return util.success(user)


    #修改倉庫的庫存、金額
    @doc(description='修改倉庫內容', tags=['倉庫'])
    @use_kwargs(warehouse_model.UserPatchSchema,location='query') #呼叫過來使用,get的話location都是query
    @marshal_with(warehouse_model.UserCommonResponse, code=201)#marshal_with的內容會出現在Response
    def patch(self, **kwargs):
        db, cursor = db_init()
        name= kwargs.get('name')
        quantity= kwargs.get('quantity')
        price=kwargs.get('price')
        sql = f"""UPDATE cart.warehouse
            SET quantity = {quantity},price ={price}
            WHERE name = '{name}';
        """
        print(sql)
        result = cursor.execute(sql)
        db.commit()
        db.close()
        if result == 0:
            return util.failure({"message": "error"})
        return util.success() 

    #刪除倉庫商品
    @doc(description='刪除倉庫商品', tags=['倉庫'])
    @use_kwargs(warehouse_model.UserDeleteScheam,location='query')
    @marshal_with(warehouse_model.UserCommonResponse, code=204)
    def delete(self, **kwargs):
        db, cursor = db_init()
        name=kwargs.get('name')
        sql = f"DELETE FROM `cart`.`warehouse` WHERE name = '{name}';"
        result = cursor.execute(sql)
        db.commit()
        db.close()
        return {'message':'success'}




        
    