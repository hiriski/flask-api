#import jsonify karena kita akan me return json yang di ambil datanya dari database
from flask import jsonify, Blueprint
from flask_restful import Resource, Api

import models # buatan sendiri

# Buat sebuah class untuk nampilin semua classnya
class MessageList(Resource):
    def get(self):
        messages = {}
        query = models.Message.select()
        for row in query:
            messages[row.id] = {
                    'content' : row.content,
                    'create_at': row.create_at
                }

        return jsonify({'messages': messages})


messages_api    = Blueprint('resources.messages', __name__)
api             = Api(messages_api)

api.add_resource(MessageList, '/messages', endpoint='messages')