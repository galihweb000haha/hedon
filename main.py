from flask import Flask, jsonify, request
import os, random, string
from flask_sqlalchemy import SQLAlchemy

# TUGAS 1
# Alfin Auzikri - 19090094
# M. Galih Fikran Syah - 19090074

# DB disimpan di tugas.db
# Untuk username dan password sama-sama menggunakan NIM.

app = Flask(__name__)
app_dir = os.path.dirname(os.path.abspath(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///{}".format(
    os.path.join(app_dir, "tugas.db"))
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=True)
    password = db.Column(db.String(120), unique=False, nullable=False)
    token = db.Column(db.String(120), unique=True, nullable=True)

    def __repr__(self):
        return '<User %r>' % self.username

@app.route('/create_db')
def create_db():
    db.create_all()
    return 'Sukses buat DB tugas.db!'


@app.route('/add_user')
def add_user():
    print('Enter your username:')
    username = input()
    print('Enter your email:')
    email = input()
    print('Enter your password:')
    password = input()

    data = User(username=username, email=email,
                password=password)
    db.session.add(data)

    db.session.commit()

    return 'User berhasil ditambahkan lewat terminal!'

@app.route('/api/v1/login', methods=['POST'])
def authentication():

    username = request.values.get('username')
    password = request.values.get('password')

    
    account = User.query.filter_by(username=username, password=password).first()
    
    if account:
        token = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=10))

        User.query.filter_by(username=username, password=password).update({'token': token})
        db.session.commit()

        data = {'result': 'true', 'msg': 'Login berhasil!!', 'token': token}
        return jsonify(data)
    else:
        data = {'result': 'false', 'msg': 'Login gagal!!'}
        return jsonify(data)


@app.route('/api/v2/users/info', methods=['POST'])
def users_info():
    token = request.values.get('token')
    account = User.query.filter_by(token=token).first()
    if account:
        return account.username
    else:
        return 'Salah bro!! tokennya..'


if __name__ == '__main__':
    app.run(debug=True, port=8080)
