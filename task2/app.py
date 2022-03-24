# 6B/19090074/M.Galih Fikran Syah
# 6D/19090094/Alfin Auzikri

# username/password = galih/galih

import os, random, string

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import jsonify
import json 
from flask_httpauth import HTTPTokenAuth
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.attributes import QueryableAttribute
from werkzeug.security import generate_password_hash, check_password_hash

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "user.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)
auth = HTTPTokenAuth(scheme='Bearer')

class User(db.Model):
    username = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    password = db.Column(db.String(80), unique=False, nullable=False, primary_key=False)
    token = db.Column(db.String(225), unique=True, nullable=True, primary_key=False)

# curl -i -X POST http://127.0.0.1:5000/api/v1/login -H 'Content-Type: application/json' -d '{"username":"galih","password":"galih"}'
@app.route("/api/v1/login", methods=["POST"])
def login():
    req = request.json
    user = User.query.filter_by(username=req['username'], password=req['password']).first()
    db.session.commit()

    if user :
        token = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=10))
        req = request.json
        user = User.query.filter_by(username=req['username']).first()

        user.token = token
        db.session.commit()
        
        return {'result': 'true', 'msg': 'Login berhasil!!', 'token': token}, 200
    else :
        return {'result': 'false', 'msg': 'Login gagal !!'}
 
@auth.verify_token
def verify_token(token):
    req = request.json
    token = req['token']
    account = User.query.filter_by(token=token).first()
    if account:
        return account.username
    else:
        return False

# curl -i -X POST http://127.0.0.1:5000/api/v2/users/info -H 'Content-Type: application/json' -d '{"token":"tokennya"}'
@app.route("/api/v2/users/info", methods=["POST"])
@auth.login_required
def info():
    return {"username": auth.current_user()},  200
