from flask import Flask, render_template, redirect, url_for, request
from data_preparation import get_data_from_csv, get_titles, get_indices, get_collection, get_popular
from content_based import calculate_similarity, get_content_based_recommendation, prepare_recommendations

app = Flask(__name__)

books, ratings, to_read, tags = get_data_from_csv()
titles = get_titles(books)
indices = get_indices(books, 'title')
collection = get_collection(books, tags)


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        option = request.form.get('recType')
        if option == 'content-based-author':
            return redirect(url_for('get_content_based_author'))
        elif option == 'content-based-author-tag':
            return redirect(url_for('get_content_based_author_tag'))
        elif option == 'collaborative-filtering':
            return redirect(url_for('get_collaborative_filtering'))
        elif option == 'popular':
            return redirect(url_for('get_popular_books'))
    return render_template('home.html')


@app.route('/content_based_author')
def get_content_based_author():
    return render_template('content-based-author.html', bookList=titles)


@app.route('/content_based_author', methods=['POST'])
def post_author_results():
    book = request.form.get('bookChoice')
    if book not in titles:
        book_error = 'please, choose a book to get recommendations'
        return render_template('content-based-author.html', book_error=book_error, bookList=titles)
    else:
        results = prepare_recommendations(get_content_based_recommendation(calculate_similarity(books['authors']),
                                                                           books['title'], indices, book), book)
        return render_template('content-based-author.html', results=results, bookList=titles, book=book)


@app.route('/content_based_author_tag')
def get_content_based_author_tag():
    return render_template('content-based-author-tag.html', bookList=titles)


@app.route('/content_based_author_tag', methods=['POST'])
def post_author_tag_results():
    book = request.form.get('bookChoice')
    if book not in titles:
        book_error = 'please, choose a book to get recommendations'
        return render_template('content-based-author-tag.html', book_error=book_error, bookList=titles)
    else:
        results = prepare_recommendations(get_content_based_recommendation(calculate_similarity(collection),
                                                                           books['title'], indices, book), book)
        return render_template('content-based-author-tag.html', results=results, bookList=titles, book=book)


@app.route('/collaborative_filtering', methods=['GET', 'POST'])
def get_collaborative_filtering():
    return render_template('collaborative-filtering.html')


@app.route('/popular_books', methods=['GET', 'POST'])
def get_popular_books():
    popular_books = get_popular(books)
    return render_template('popular.html', popular_books=popular_books)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000, debug=True)
