from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api  = Api(app)

users = {}

class User(Resource):
    # metode-metode yang ada di classnya udah otomatis restfull seperti get put dll
    def get(self, user_id):
        return {'name':users[user_id]} 

    # Metode untu memasukan data
    def put(self, user_id):
        users[user_id] = request.form['user']
        return {'name':users[user_id]}

# Nah untuk nge add ini kita pake dibawah ini
# Parameter pertama nama class nya
# Parameter kedua urlnya
api.add_resource(User, '/user/<int:user_id>')

# Untuk memastikan fungsi yang mau kita jalankan ada di file ini
if __name__ == '__main__':
    app.run(debug=True)