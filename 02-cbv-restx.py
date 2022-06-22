from flask import request, Flask
from flask_restx import Api, Resource

app = Flask(__name__)
api = Api(app)
books_ns = api.namespace('')

books = {
    1: {
        "name": "Harry Potter",
        "year": 2000,
        "author": "Joan Rouling"
    },
    2: {
        "name": "Le Comte de Monte-Cristo",
        "year": 1844,
        "author": "Aleksandre Dumas"
    }
}


@books_ns.route('/books')
class BooksView(Resource):
    def get(self):
        return books, 200

    def post(self):
        req_json = request.json
        books[len(books) + 1] = req_json
        return "", 201


@books_ns.route('/books/<int:bid>')
class BookView(Resource):
    def get(self, bid):
        return books[bid], 200

    def delete(self, bid):
        del books[bid]
        return "", 204


if __name__ == "__main__":
    app.run(debug=False)
