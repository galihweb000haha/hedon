#curl -u john:hello http://127.0.0.1:5000/
#curl -u galih:galih http://127.0.0.1:5000/

from app import app
from app import auth
from flask import jsonify
from app.model.User import User
from werkzeug.security import generate_password_hash, check_password_hash

# users = {
#     "john": generate_password_hash("hello"),
#     "susan": generate_password_hash("bye"),
#     "galih": generate_password_hash("galih")
# }

class Authentincation:
    @auth.verify_password
    def verify_password(self, username, password):
        user = User()
        users = user.getUser_array()
        if username in users and \
                check_password_hash(users.get(username), password):
            return True
        else :
            return False
