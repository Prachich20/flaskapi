from flask import Flask
import json
import os
import pytest
from flask_sqlalchemy import SQLAlchemy

BASE_URL = 'http://127.0.0.1:5000/'


def create_app():
    flask_app = Flask(__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))
    DB_url = 'sqlite:///' + os.path.join(basedir, 'survey.db')
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = DB_url
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    flask_app.app_context().push()
    db = SQLAlchemy(flask_app)
    db.init_app(flask_app)
    db.create_all()
    return flask_app


@pytest.fixture
def app():
    app = create_app()
    return app


@pytest.fixture
def client(app):
    return app.test_client()

def test_results():
    url = '/results'
    response = client.post(url, data=json.dumps({"id": 1}))
    assert response.status_code == 200
    assert response.mode == 4.4
    assert response.median == 4.4
    assert response.mean == 4.13
    assert response.count == 18


def test_stat(client):
    url = 'stat/<stat_id>'
    response = client.post(url, data=json.dumps({"name": "Test Data"}))
    assert response.status_code == 200


def test_removesurvey(client):
    response = client.post('/survey/<id>/',data=json.dumps({"id": 1}))
    assert response.status_code == 200


def test_addsurvey(client):
    # url = BASE_URL + '/'
    response = client.post('/survey/', data=json.dumps({"name": "test"}))
    assert response.status_code == 200

def test_survey(client):
    # url = BASE_URL + '/'
    response = client.get('/')
    assert response.status_code == 200
