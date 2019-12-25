#import jsonify karena kita akan me return json yang di ambil datanya dari database
from flask import jsonify, Blueprint
from flask_restful import Resource, Api

import models # buatan sendiri

# Buat sebuah class untuk nampilin semua classnya
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


blogs_api   = Blueprint('resources.blogs', __name__)
api         = Api(blogs_api)
api.add_resource(BlogList, '/blogs', endpoint="blogs")