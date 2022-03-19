import os, random, string

from flask import Flask, jsonify, render_template, request, redirect

# model
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.attributes import QueryableAttribute

# auth
from flask_httpauth import HTTPBasicAuth


# token
from flask_httpauth import HTTPTokenAuth
token = HTTPTokenAuth(scheme='Bearer')

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "my_data.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

auth = HTTPBasicAuth()

from app.model import User
from app.lib import authentincation
from app.lib import tokenisation
from app.api import Api



