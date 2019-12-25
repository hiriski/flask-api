#import jsonify karena kita akan me return json yang di ambil datanya dari database
from flask import jsonify, Blueprint
from flask_restful import Resource, Api

import models # buatan sendiri

# Buat sebuah class untuk nampilin semua blognya
class BlogList(Resource):
    def get(self):

        # siapin variable kosong dengan type data dictionary
        blogs = {}

        # ambil data dari database
        query = models.Blog.select()
        for row in query:
            blogs[row.id] = {
                'title': row.title,
                'create_at' : row.create_at
                }
        
        # Return dalam bentuk JSON
        return jsonify({'blog': blogs})


# Class untuk blog singular nya berdasarkan id tertentu
# Misal  http:127.0.0.1/api/v1/message/1
class Blog(Resource):
    def get(self, id):
        # karena akan mengambil berdasarkan id maka metode yang dipake .get_by_id
        blog_list = models.Blog.get_by_id(id)
        return jsonify({
                'title':blog_list.title,
                'create_at': blog_list.create_at
            })


blog_api   = Blueprint('resources.blog', __name__)
api         = Api(blog_api)

api.add_resource(BlogList, '/blog', endpoint="blogs")
api.add_resource(Blog, '/blog/<int:id>', endpoint='blog')