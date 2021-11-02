from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from flask import Flask, jsonify, request, render_template
import sqlite3

# instead of a method at a time, you can have a resource and then bind urls with them
class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field is required")

    @jwt_required()
    def get(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "select * from items where name = ?"

        result = cursor.execute(query, (name,))
        row = result.fetchone()

        connection.close()
        if row:
            return {'item': {"name": row[0], 'price': row[1]}}, 200
        return {'message': "item not found"}, 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {'message', "An item with name {} already exits".format(name)}, 400

        data = request.get_json()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'item deleted'}

    # PUT method is always idempotent
    def put(self, name):

        data = Item.parser.parse_args()

        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item

class ItemsList(Resource):
    def get(self):
        return {'item': items}
