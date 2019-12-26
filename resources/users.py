from flask import jsonify, Blueprint, abort
from flask_restful import  Resource, Api, reqparse, fields, marshal, marshal_with

# import JWT
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity)

# import hash password
from hashlib import md5

import models 

user_fields = {
    'username'      : fields.String,
    # akses token
    'access_token'  : fields.String

    # karena masalah keamanan saya nggak mau nampilin password usernya
    # ketika berhasil register
    #'password'  : fields.String
}

class BaseUser(Resource):
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

class UserList(BaseUser):
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
                password = md5(new_user_password.encode('utf-8')).hexdigest()
                )

            # ngirim token berarti butuh sesuatu di user_fields nya

            # Saya butuh mendapatkan akses token. Saya bisa dapetin dari fungsi create_access_token dari JWT
            # untuk parameternya disini identity dan valuenya apa saja asalkan unik
            access_token = create_access_token(identity=new_user_username)

            # selipkan akses token
            user.access_token = access_token
            return marshal(user, user_fields) 
        else:
            return {'pesan':'Sorry, username ini sudah dipake orang!'}


class User(BaseUser):
    def post(self):
        kwargs = self.reqparse.parse_args()
        # insert data user
        user_username_registered = kwargs.get("username")
        user_password_registered = kwargs.get("password")
        # login
        # uji apakah password dan usernamenya benar
        try:
            # buat variabel untuk password yang sudah di hash
            hash_password = md5(user_password_registered.encode('utf-8')).hexdigest()
            # uji metode sign in
            user = models.User.get( (models.User.username == user_username_registered) & (models.User.password == hash_password) )
 
        except models.User.DoesNotExist: 
            return {'pesan':'User or password is wrong bro!'}

        else:
            access_token = create_access_token(identity=user_username_registered)
            return {
                'pesan':'Singin success!',
                'access_token':access_token
                }


    # metode get untuk sign in dan mendapatkan token

    # untuk memproteksi bagian menggunakan token kita bisa ngasih @jwt_required
    # artinya nggak semua orang boleh mengakses bagian ini, tapi hanya yang mengirim token
    @jwt_required
    def get(self):
        return {'pesan':"Ini bagian yang terproteksi"}

users_api    = Blueprint('resources.users', __name__)
api          = Api(users_api)

api.add_resource(UserList, '/user/register', endpoint="user/register")
api.add_resource(User, '/user/signin', endpoint="user/signin")