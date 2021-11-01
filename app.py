from flask import Flask, jsonify, request, render_template
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

items = [

]

stores = [
    {
        "name": "My Store",
        "items": [
            {
                "name": "item1",
                "price": 10
            }
        ]
    }
]

# instead of a method at a time, you can have a resource and then bind urls with them
class Item(Resource):
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {'message', "An item with name {} already exits".format(name)}, 400

        data = request.get_json()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

class ItemsList(Resource):
    def get(self):
        return {'item': items}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemsList, '/items')

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/store', methods = ['POST'])
def create_store():
    request_data = request.get_json()
    newstore = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(newstore)
    return jsonify(newstore)

@app.route('/store/<string:name>')
def get_store(name):
    for st in stores:
        if st["name"] == name:
            return jsonify(st)
    return jsonify({"message": 'store not found'})

@app.route('/store')
def get_stores():
    return jsonify(stores)


@app.route('/store/<string:name>/item', methods = ['POST'])
def create_item_in_store(name):
    request_data = request.get_json()
    for st in stores:
        if st["name"] == name:
            new_item = {
                'name' : request_data['name'],
                'price': request_data['price']
            }
            st["items"].append(new_item)
            return jsonify(st)
    return jsonify({"message": 'store not found'})


@app.route('/store/<string:name>/item')
def get_item_in_store(name):
    for st in stores:
        if st["name"] == name:
            return jsonify({"items": st['items']})
    return jsonify({"message": 'store not found'})


if __name__ == '__main__':
    app.run(port=9090)
