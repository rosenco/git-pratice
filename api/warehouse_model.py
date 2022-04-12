
from marshmallow import Schema, fields

#UserGetSchema
class UserGetSchema(Schema):
    name=fields.Str()#希望name的格式是str

# UserPostScheam
class UserPostSchema(Schema):
    name = fields.Str(doc="name", example="string", required=True)
    price = fields.Str(doc="number", example="string", required=True)
    quantity=fields.Str(required=True)

#UPdate_Schema
class UserPatchSchema(Schema):
    name = fields.Str(doc="name", example="string", required=True)
    price = fields.Str(doc="number", example="string", required=True)
    quantity=fields.Str(required=True)  

# UserDeleteScheam
class UserDeleteScheam(Schema):
    name = fields.Str(doc="name", example="string", required=True)
    
#GetResponse
class UserGetResponse(Schema):
    message = fields.Str(example="success")
    data = fields.List(fields.Dict())
    warehouse=fields.Str()
    datatime = fields.Str()
    

#PostResponse
class UserPostResponse(Schema):
    message = fields.Str(example="success")
    data = fields.Dict()
    datatime = fields.Str()

#Response
class UserCommonResponse(Schema):
    message = fields.Str(example="success")
    data = fields.List(fields.Dict())
    datatime = fields.Str()