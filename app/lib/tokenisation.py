# curl -H "Authorization: Bearer secret-token-1" http://127.0.0.1:5000/
# curl -H "Authorization: Bearer au98YH899uUJOIH980y" http://127.0.0.1:5000/
from app import app
from app import token
from flask import Flask
from app.model.User import User


class Tokenisation:
    @token.verify_token
    def verify_token(self, token):
        user = User()
        tokens = user.getToken()
        if token in tokens:
            return True
        else:
            return False
