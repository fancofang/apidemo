from flask import request, jsonify
from sqlalchemy import or_
from app.api.v1 import api_v1
from app.forms import BookSearchForm
from app.libs.error_code import BookException, ParameterException
from app.models import Book


@api_v1.route('/book/search')
def search():
    """Searching book on keyword

    :Url: http://3.9.215.67:9999/api/v1/book/search?q=<keyword>
    :Method: GET
    :Authorization: Bearer
    :param: something about the book. For exmaple book name, author, publisher, isbn, isbn13
    :return: the set of result
    """
    data = request.args.to_dict()
    form = BookSearchForm(data=data)
    form.validate_for_api()
    q = '%' + form.q.data + '%'
    books = Book.query.filter(or_(Book.title.ilike(q),
                                  Book.publisher.ilike(q),
                                  Book.authors.ilike(q),
                                  Book.isbn.ilike(q),
                                  Book.isbn13.ilike(q)
                                  )).all()
    if books == []:
        return BookException()
    books = [book.hide('id','text_reviews_count') for book in books]
    return jsonify(books)

@api_v1.route('/book/<isbn>')
def detail(isbn):
    """The detail of book

    :url: http://3.9.215.67:9999/api/v1/book/{isbn or isbn13}
    :method: GET
    :authorization: Bearer
    :param: isbn or isbn13
    :return: detail
    """
    if isbn.isdigit() is not True:
        return ParameterException()
    if len(isbn) == 10:
        book = Book.query.filter_by(isbn=isbn).first()
    else:
        book = Book.query.filter_by(isbn13=isbn).first()
    if book is None:
        return BookException()
    return jsonify(book)