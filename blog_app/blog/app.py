from flask import Flask, jsonify, request

from blog.commands import CreateArticleCommand
from blog.queries import GetArticleByIDQuery, ListArticlesQuery

app = Flask(__name__)


@app.route('/create-article/', methods=['POST'])
def create_article():
    cmd = CreateArticleCommand(**request.json)
    return jsonify(cmd.execute().dict())


@app.route('/article/<article_id>/', methods=['GET'])
def get_article(article_id):
    query = GetArticleByIDQuery(id=article_id)
    return jsonify(query.execute().dict())


@app.route('/article-list/', methods=['GET'])
def list_articles():
    query = ListArticlesQuery()
    records = [record.dict() for record in query.execute()]
    return jsonify(records)


if __name__ == '__main__':
    app.run()
