import json
import pathlib

import pytest
from jsonschema import validate, RefResolver

from blog.app import app
from blog.models import Article


@pytest.fixture
def client():
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client


def validate_payload(payload, schema_name):
    """
    Validate payload with selected schema
    """
    schemas_dir = str(f'{pathlib.Path(__file__).parent.absolute()}/schemas')
    schema = json.loads(pathlib.Path(f'{schemas_dir}/{schema_name}').read_text())
    validate(
        payload,
        schema,
        resolver=RefResolver(
            'file://' + str(pathlib.Path(f'{schemas_dir}/{schema_name}').absolute()),
            schema,  # it's used to resolve file: inside schemas correctly
        ),
    )


def test_create_article(client):
    """
    GIVEN request data for new article
    WHEN endpoint /create-article/ is called
    THEN it should return Article in json format matching schema
    """
    data = {'author': 'john@doe.com', 'title': 'New Article', 'content': 'Some extra awesome content'}
    response = client.post(
        '/create-article/',
        data=json.dumps(data),
        content_type='application/json',
    )

    validate_payload(response.json, 'Article.json')


def test_get_article(client):
    """
    GIVEN ID of article stored in the database
    WHEN endpoint /article/<id-of-article>/ is called
    THEN it should return Article in json format matching schema
    """
    article = Article(author='jane@doe.com', title='New Article', content='Super extra awesome article').save()
    response = client.get(
        f'/article/{article.id}/',
        content_type='application/json',
    )

    validate_payload(response.json, 'Article.json')


def test_list_articles(client):
    """
    GIVEN articles stored in the database
    WHEN endpoint /article-list/ is called
    THEN it should return list of Article in json format matching schema
    """
    Article(author='jane@doe.com', title='New Article', content='Super extra awesome article').save()
    response = client.get(
        '/article-list/',
        content_type='application/json',
    )

    validate_payload(response.json, 'ArticleList.json')
