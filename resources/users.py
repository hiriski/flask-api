from flask import jsonify, Blueprint, abort
from flask_restful import  Resource, Api, reqparse, fields, marshal, marshal_with

# import hash password
from hashlib import md5

import models 

user_fields = {
    'username'  : fields.String,

    # karena masalah keamanan saya nggak mau nampilin password usernya
    # ketika berhasil register
    #'password'  : fields.String
}

class UserList(Resource):
    # Fungsi ini akan otomatis terpanggil ketika BlogListnya dijalankan
    def __init__(self):
        self.reqparse = reqparse.RequestParser()

        # untuk aturannya sendiri dan apa data yang mau kita terima kita simpan di .add_argument()
        self.reqparse.add_argument(
            'username',
            required    = True,
            help        = 'Username wajib ada', 
            location    = ['form', 'json']
        )
        self.reqparse.add_argument(
            'password',
            required    = True,
            help        = 'Password wajib ada', 
            location    = ['form', 'json']
        )
        super().__init__() # pastiin dia manggil fungsi __init__ dari parentnya juga


    # method post untuk nge-post data
    def post(self):
        kwargs = self.reqparse.parse_args()

        # insert data user
        new_user_username = kwargs.get("username")
        new_user_password = kwargs.get("password")

        # Uji dulu apakah usernya sudah ada
        try:
            models.User.select().where(models.User.username == new_user_username).get()
        except models.User.DoesNotExist:
            # daftarin usernya
            user = models.User.create(
                username = new_user_username,
                # hash password usernya
                password = md5(new_user_username.encode('utf-8')).hexdigest()
                )
            return marshal(user, user_fields) 
        else:
            raise Exception('User ini sudah terdaftar bro')


class User(Resource):
    pass


users_api    = Blueprint('resources.users', __name__)
api          = Api(users_api)

api.add_resource(UserList, '/user/register', endpoint="user/register")
api.add_resource(User, '/user/login', endpoint="user/login")