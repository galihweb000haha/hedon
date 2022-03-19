import os, random, string

from flask import Flask, jsonify
from flask import render_template
from flask import request
from flask import redirect

from authentication import verify_password

from User import update_token
from User import getUser
# from token import verify_token

# from flask_sqlalchemy import SQLAlchemy

# project_dir = os.path.dirname(os.path.abspath(__file__))
# database_file = "sqlite:///{}".format(os.path.join(project_dir, "my_data.db"))

app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = database_file
# db = SQLAlchemy(app)

# class User(db.Model):
#     id_user = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(128), unique=True, nullable=False)
#     password = db.Column(db.String(128), unique=False, nullable=False)
#     token = db.Column(db.String(255), unique=True, nullable=True)

#     def __repr__(self):
#         return '<User %r>' % self.username

# ini tidak perlu dijalankan
# @app.route('/createDB')
# def createDB():
#     db.create_all()
#     return 'New Databases has been created sucessfully!'

# ini tidak perlu dijalankan
# @app.route('/addUser')
# def addUser():
#     print('Enter username:')
#     username = input()
#     print('Enter password:')
#     password = input()
#     data = User(username=username, password=password)
#     db.session.add(data)
#     db.session.commit()
#     return 'New User has been added sucessfully!'

@app.route('/api/v1/getUser', methods=['GET'])
def get_user():
    return getUser()


@app.route('/api/v1/login', methods=['POST'])
def authentication():
    username = request.values.get('username')
    password = request.values.get('password')

    if (verify_password(username, password) ) :
        # update new token
        token = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=10))
        # database
        update_token(token)
        # return token
        data = {"token":token}
        return jsonify(data)

@app.route('/api/v2/users/info', methods=['POST'])
def getInfo():
    token = request.values.get('token')
    if (verify_token()) :
        # show user information
        return "ok"

if __name__ == '__main__':
    app.run(debug = True)
