import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


basedir = os.path.abspath(os.path.dirname(__file__))
DB_url = 'sqlite:///' + os.path.join(basedir, 'survey.db')
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = DB_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Survey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))

    def __init__(self,name):
        self.name = name

    def __repr__(self):
        return '<Survey {}>'.format(self.id)


class Observation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    survey_id = db.Column(db.Integer, db.ForeignKey('survey.id'), nullable=False)
    value = db.Column(db.Float)
    frequency = db.Column(db.Integer)

    def __init__(self, survey_id, value, frequency):
        self.survey_id = survey_id
        self.value = value
        self.frequency = frequency

    def __repr__(self):
        return '<Observation {}>'.format(self.id)