from flask import Flask, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():
    articles = Article.query.all()
    serialized_articles = [article.serialize() for article in articles]
    return jsonify(serialized_articles)

@app.route('/articles/<int:id>')
def show_article(id):
    if 'page_views' not in session:
        session['page_views'] = 0

    session['page_views'] += 1

    articles_data = {
        'id': id,
        'title': f'Article {id}',
        'content': f'Content of Article {id}',
        'author': 'John Doe',
        'minutes_to_read': 5,
        'preview': f'Preview of Article {id}',
        'date': '2022-01-01',
    }

    if session['page_views'] <= 3:
        return jsonify(articles_data)

    return jsonify({'message': 'Maximum pageview limit reached'}), 401

if __name__ == '__main__':
    app.run(port=5555)
