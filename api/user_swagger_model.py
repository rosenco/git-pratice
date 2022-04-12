
from marshmallow import Schema, fields

#UserGetSchema
class UserGetSchema(Schema):
    name=fields.Str()#希望name的格式是str

# UserPostScheam
class UserPostSchema(Schema):
    name = fields.Str(doc="name", example="string", required=True)
    number = fields.Str(doc="number", example="string", required=True)


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
 

#UPdate_Schema
class UserPatchSchema(Schema):
    name = fields.Str(doc="name", example="string", required=True)
    number = fields.Str(doc="number", example="string")
    

class LoginSchema(Schema):
    account = fields.Str(doc="account", example="string", required=True)
    password = fields.Str(doc="password", example="string", required=True)

class checkoutResponse(Schema):
    message = fields.Str(example="success")
    datatime = fields.Str(example="1970-01-01T00:00:00.000000")
    data = fields.Dict(fields.Dict())


class UserLoginResponse(Schema):
    message = fields.Str(example="success")
    datatime = fields.Str(example="1970-01-01T00:00:00.000000")
    data = fields.Dict()