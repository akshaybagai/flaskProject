import sqlite3
from flask_restful import Resource, reqparse

class User:

    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(self, username):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "select * from users where username = ?"
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        if row:
            user = User(*row)
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(self, id):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "select * from users where id = ?"
        result = cursor.execute(query, (id,))
        row = result.fetchone()
        if row:
            user = User(*row)
        else:
            user = None

        connection.close()
        return user


class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required= True,
                        help="This field cannot be blank")

    parser.add_argument('password',
                        type=str,
                        required= True,
                        help="This field cannot be blank")

    def post(self):

        data = UserRegister.parser.parse_args();

        if User.find_by_username(data['username']):
            return {"message": "user already exists"}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "insert into users values (null, ?, ?)"
        cursor.execute(query, (data['username'], data['password'],))

        connection.commit()
        connection.close()

        return {"message": "user created successfully"}, 201