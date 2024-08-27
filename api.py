from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
api = Api(app)


class ItemModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    date_create = db.Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return f"Items(id = {self.id}, name = {self.name}, price = {self.email}, date = {self.date_create})"


item_args = reqparse.RequestParser()
item_args.add_argument('name', type=str, required=True, help="Name cannot be blank")
item_args.add_argument('price', type=int, required=True, help="price cannot be blank or a string")

itemFields = {'id': fields.Integer,
              'name': fields.String,
              'price': fields.Integer,
              'date_create': fields.DateTime}


class Items(Resource):
    @marshal_with(itemFields)
    def get(self):
        users = ItemModel.query.all()
        return users

    @marshal_with(itemFields)
    def post(self):
        args = item_args.parse_args()
        item = ItemModel(name=args['name'], price=args['price'])
        db.session.add(item)
        db.session.commit()
        items = ItemModel.query.all()
        return items, 201


class Item(Resource):
    @marshal_with(itemFields)
    def get(self, id):
        item = ItemModel.query.filter_by(id=id).first()
        if not item:
            abort(404, message="User not found")
        return item

    @marshal_with(itemFields)
    def patch(self, id):
        args = item_args.parse_args()
        item = ItemModel.query.filter_by(id=id).first()
        if not item:
            abort(404, "user not found")
        item.name = args["name"]
        item.price = args["price"]
        db.session.commit()
        return item

    @marshal_with(itemFields)
    def delete(self, id):
        item = ItemModel.query.filter_by(id=id).first()
        if not item:
            abort(404, "user not found")
        db.session.delete(item)
        db.session.commit()
        items = ItemModel.query.all()
        return item


api.add_resource(Items, '/api/items/')
api.add_resource(Item, '/api/items/<int:id>')


@app.route('/')
def home():
    return '<h1>Flask REST API</h1>'


if __name__ == '__main__':
    app.run(debug=True)
