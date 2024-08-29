from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
api = Api(app)


class ItemModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    type = db.Column(db.String(), nullable=False)
    colour = db.Column(db.String(), nullable=False)
    date_create = db.Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return f"Items(id = {self.id}, name = {self.name}, price = {self.price},type = {self.type}, colour = {self.colour}, date = {self.date_create})"


item_args = reqparse.RequestParser()
item_args.add_argument('name', type=str, required=True, help="Name cannot be blank")
item_args.add_argument('price', type=int, required=True, help="price cannot be blank or a string")
item_args.add_argument('type', type=str, required=True, help="type cannot be blank")
item_args.add_argument('colour', type=str, required=True, help="type cannot be blank")

itemFields = {'id': fields.Integer,
              'name': fields.String,
              'price': fields.Integer,
              'type': fields.String,
              'colour': fields.String,
              'date_create': fields.DateTime}


class Items(Resource):
    @marshal_with(itemFields)
    def get(self):  # фильтрация
        name_filter = request.args.get("name")
        type_filter = request.args.get("type")
        price_filter = request.args.get("price")
        colour_filter = request.args.get("colour")
        sorts = request.args.get("sort")
        items_query = ItemModel.query
        if name_filter:
            items_query = items_query.filter(ItemModel.name.like(f"%{name_filter}%"))
        if type_filter:
            items_query = items_query.filter(ItemModel.type == type_filter)
        if colour_filter:
            items_query = items_query.filter(ItemModel.colour == colour_filter)
        if price_filter:
            if price_filter[0] == "-":
                items_query = items_query.filter(ItemModel.price <= int(price_filter[1:]))
            else:
                items_query = items_query.filter(ItemModel.price <= int(price_filter))

        if sorts:  # фильтрациф по порядку убивания  если sort=-var и можно комбинировать через sort=name,-price
            for sort in sorts.split(","):
                descending = sort[0] == "-"
                if descending:
                    field = getattr(ItemModel, sort[1:])
                    items_query = items_query.order_by(desc(field))
                else:
                    field = getattr(ItemModel, sort)
                    items_query = items_query.order_by(field)

        items = items_query.all()
        return items

    @marshal_with(itemFields)
    def post(self):
        args = item_args.parse_args()
        item = ItemModel(name=args['name'], price=args['price'], type=args["type"], colour=args["colour"])
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
        item.type = args["type"]
        item.colour = args["colour"]
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
    return "<h1>Flask Api</h1>"


if __name__ == '__main__':
    app.run(debug=True)
