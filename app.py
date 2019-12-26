from flask import Flask, request
from flask_restful import Resource

# import resources yang udah di bikin
from resources.blog import blog_api
from resources.users import users_api

# import JWT
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity)


import models

app = Flask(__name__)
app.register_blueprint(blog_api, url_prefix='/api/v1')
app.register_blueprint(users_api, url_prefix='/api/v1')

# api  = Api(app)
# api.add_resource(blog.BlogList, '/blog')
# api.add_resource(message.MessageList, '/message')

# Untuk memastikan fungsi yang mau kita jalankan ada di file ini
if __name__ == '__main__':
    
    # panggil function initialize() dari models
    models.initialize()
    app.run(debug=True)