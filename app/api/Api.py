import os, random, string
from app import app
from app.lib.tokenisation import Tokenisation
from app.lib.authentincation import Authentincation
from app.model.User import User

from flask import jsonify
from flask import (Flask, render_template, url_for, request, abort, redirect, make_response, session, flash, abort, jsonify)

@app.route('/api/v1/login', methods=['POST'])
def authentication():
    username = request.values.get('username')
    password = request.values.get('password')
    authentincation = Authentincation()
    if (authentincation.verify_password(username, password) ) :
        # update new token
        token = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=10))
        # database
        user = User()
        user.updateToken(username, password, token)
        # return token
        data = {"token":token}
        return jsonify(data)
    data = {"status": "failed"}
    return jsonify(data)

@app.route('/api/v2/users/info', methods=['POST'])
def getInfo():
    token = request.values.get('token')
    if (verify_token()) :
        # show user information
        return "ok"

@app.route('/api/getUser', methods=['GET'])
def getUser():
    user = User()
    return user.getUser_array()

@app.route('/api/addUser', methods=['GET'])
def addUser():
    user = User()
    return user.addUser()