#import jsonify karena kita akan me return json yang di ambil datanya dari database
from flask import jsonify, Blueprint, abort
from flask_restful import  Resource, Api, reqparse, fields, marshal, marshal_with

# Menambahkan 3 module yaitu fields, marsha; dan marshal_with
# dengan ketiga module bantuan ini lebih mudah memberi respon dan lebih konsisten

# penggunaan fields
blog_fields = {
    'id'        : fields.Integer,
    'title'     : fields.String,
    'content'   : fields.String,
    'create_at' : fields.String #suatu saat ganti jadi Datetime
}

# Function get or abort
def get_or_abort(id):
    try:
        foo = models.Blog.get_by_id(id)
    except models.Blog.DoesNotExist:
        # Kalau id blog tidak ditemukan lempar ke 404
        abort(404)
    else:
        # Kalau datanya ada return foo nya langsung
        return foo



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
        # return jsonify({
        #         'sucess':'Data berhasil di POST',
        #         'judul_blog':foo.title,
        #         'konten_blog':foo.content,
        #         'tanggal':foo.create_at
        #     })

        # Ganti return dsini menggunakan marshal
        return marshal(foo, blog_fields)
        

    def get(self):

        # siapin variable kosong dengan type data dictionary
        # blogs = {}

        # ambil data dari database
        # query = models.Blog.select()
        # for row in query:
        #     blogs[row.id] = {
        #         'title': row.title,
        #         'create_at' : row.create_at
        #         }
        

        #*** PEMGGUNAAN MARSHAL ***#
        # Jika sebelumnya saya harus nge for loop masing-masing datanya seperti di atas dan dipindahkan ke dictionary menggunakan jsonify
        # sekarang saya bisa lebih mudah melakukan itu dengan menggunakan marhsal

        blog_list = [marshal(blog, blog_fields) for blog in models.Blog.select()]
        # marhsal butuh 2 parameter
        # parameter 1 namanya
        # parameter 2 data fields nya
 

        # Return dalam bentuk JSON
        return jsonify({'blog': blog_list})


# Class untuk blog singular nya berdasarkan id tertentu
# Misal  http:127.0.0.1/api/v1/message/1
class Blog(Resource):

    # menggunakan Marshal with
    @marshal_with(blog_fields)

    def get(self, id):
        # karena akan mengambil berdasarkan id maka metode yang dipake .get_by_id
        # blog_list = models.Blog.get_by_id(id)
        # return jsonify({
        #         'title':blog_list.title,
        #         'create_at': blog_list.create_at
        #     })

        # misalnya saya mengakses http:127.0.0.1/api/v1/blog/1 bisa karena memang id 1 ada
        # tapi bagaimana jika yang di akses id yang tidak ada berarti harus dilemparkan ke halaman 404 dong
        # nah untuk itu saya akan me return function disini -- JADI RETURN BUKAN JSONIFY LAGI
        return get_or_abort(id)
        
blog_api    = Blueprint('resources.blog', __name__)
api         = Api(blog_api)

api.add_resource(BlogList, '/blog', endpoint="blogs")
api.add_resource(Blog, '/blog/<int:id>', endpoint='blog')