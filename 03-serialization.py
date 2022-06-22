from flask import request, Flask
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    author = db.Column(db.String(100))
    year = db.Column(db.Integer)


class BookSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    author = fields.Str()
    year = fields.Int()


book_schema = BookSchema()
books_schema = BookSchema(many=True)


api = Api(app)
book_ns = api.namespace('')


b1 = Book(id=1, name = "Harry Potter", author="Joan Rouling", year=1992)
b2 = Book(id=2, name = "Le Comte de Monte-Cristo", author="Aleksandre Dumas", year=1844)

db.create_all()

with db.session.begin():
    db.session.add_all([b1, b2])


@book_ns.route('/books')
class BooksView(Resource):
    def get(self):
        all_books = db.session.query(Book).all()
        return books_schema.dump(all_books), 200

    def post(self):
        req_json = request.json
        new_book = Book(**req_json)
        with db.session.begin():
            db.session.add(new_book)
        return "", 201


@book_ns.route('/books/<int:uid>')
class BookView(Resource):
    def get(self, uid: int):
        try:
            book = db.session.query(Book).filter(Book.id == uid).one()
            return book_schema.dump(book), 200
        except Exception as e:
            return str(e), 404

    def put(self, uid):
        book = db.session.query(Book).get(uid)
        req_json = request.json
        book.name = req_json.get("name")
        book.author = req_json.get("author")
        book.age = req_json.get("age")
        db.session.add(book)
        db.session.commit()
        return "", 204

    def put(self, uid:int):
        book = db.session.query(Book).get(uid)
        req_json = request.json
        if "name" in req_json:
            book.name = req_json.get("name")
        if "author" in req_json:
            book.author = req_json.get("author")
        if "age" in req_json:
            book.age = req_json.get("age")
        db.session.add(book)
        db.session.commit()
        return "", 204

    def delete(self, uid:int):
        book = db.session.query(Book).get(uid)
        db.session.delete(book)
        db.session.commit()
        return "", 204


if __name__ == "__main__":
    app.run(debug=False)
