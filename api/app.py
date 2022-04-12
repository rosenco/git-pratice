from pydoc import doc
from apispec import APISpec
import flask
from flask_restful import Api
from apispec.ext.marshmallow import MarshmallowPlugin #序列檢查
from flask_apispec.extension import FlaskApiSpec
from flask_jwt_extended import JWTManager 
from final import  Cart, checkout,signin
from warehouse import warehouse


app=flask.Flask(__name__)
api=Api(app)
print(app.config)
app.config['DEBUG']=True

app.config.update({
    'APISPEC_SPEC':APISpec(
        title='Awesome Project',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL':'/swagger/',
    'APISPEC_SWAGGER_UI_URL':'/swagger-ui/'    
})
docs=FlaskApiSpec(app)

api.add_resource(Cart,'/Cart')
docs.register(Cart)
api.add_resource(warehouse,'/warehouse')
docs.register(warehouse)
api.add_resource(checkout,'/checkout')
docs.register(checkout)
api.add_resource(signin,'/signin')
docs.register(signin)


if __name__=='__main__':
    jwt = JWTManager().init_app(app)
    app.run(host='127.0.0.1',port=10018)
