#import jsonify karena kita akan me return json yang di ambil datanya dari database
from flask import jsonify, Blueprint
from flask_restful import Resource, Api, reqparse

import models # buatan sendiri

# Buat sebuah class untuk nampilin semua blognya
class BlogList(Resource):

    # Fungsi ini akan otomatis terpanggil ketika BlogListnya dijalankan
    def __init__(self):
        self.reqparse = reqparse.RequestParser()

        # untuk aturannya sendiri dan apa data yang mau kita terima kita simpan di .add_argument()
        self.reqparse.add_argument(
            'title',
            required    = True, # field ini wajib, jika kosong user akan menerima pesan error
            help        = 'Konten wajib ada', # pesan error
            location    = ['form', 'json'] # kalau di postman x-www-form-urlendoded
        )
        
        # ini hampir sama kek di atas
        self.reqparse.add_argument(
            'content',
            required    = True, 
            help        = 'Content blog harus ada bro',
            location    = ['form', 'json']
        )

        # ini hampir sama kek di atas
        self.reqparse.add_argument(
            'create_at',
            required    = True, 
            help        = 'Tanggal harus ada bro',
            location    = ['form', 'json']
        )

        super().__init__() # pastiin dia manggil fungsi __init__ dari parentnya juga
    
    # method post untuk nge-post data
    def post(self):
        args = self.reqparse.parse_args()

        # insert data
        # nanti jadinya akan seperti content='Ini judul blog' akan jadi key dan value
        # itulah yang akan jadi parameter dari args
        foo = models.Blog.create(**args)
        return jsonify({
                'sucess':'Data berhasil di POST',
                'judul_blog':foo.title,
                'konten_blog':foo.content,
                'tanggal':foo.create_at
            })


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


blog_api    = Blueprint('resources.blog', __name__)
api         = Api(blog_api)

api.add_resource(BlogList, '/blog', endpoint="blogs")
api.add_resource(Blog, '/blog/<int:id>', endpoint='blog')