from app import app, db
from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id_user = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), unique=False, nullable=False)
    token = db.Column(db.String(255), unique=True, nullable=True)

    def __repr__(self):
        return json.dumps(self.__dict__)

    def createDB(self):
        db.create_all()
        return 'New Databases has been created sucessfully!'

    def addUser(self):
        print('Enter username:')
        username = input()
        print('Enter password:')
        password = input()
        password = generate_password_hash(password)
        data = User(username=username, password=password)
        db.session.add(data)
        db.session.commit()
        return 'New User has been added sucessfully!'

    def getUser(self):
        users = User.query.all()
        array_users = []
        for user in users:
            dict_users = {}
            dict_users.update({"username": user.username, "password": user.password, "token": user.token})
            array_users.append(dict_users)
        return jsonify(array_users), 200, {'content-type':'application/json'} 
        
    def getUser_array(self):
        users = User.query.all()
        dict_users = {}
        for user in users:
            dict_users.update({user.username: generate_password_hash(user.password)})
        return dict_users

    def updateToken(self, username, password, token):
        User.query.filter_by(username=username, password=password).update({'token': token})
        db.session.commit()
        return True