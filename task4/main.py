import os
from flask import Flask, flash, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# datetime.utcnow()
from uuid import uuid4


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app_dir = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
project_dir = os.path.dirname(os.path.abspath(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///{}".format(os.path.join(project_dir, "upload.db"))
db = SQLAlchemy(app)

if not os.path.exists(os.path.join(app_dir, app.config['UPLOAD_FOLDER'])):
    os.makedirs(os.path.join(app_dir, app.config['UPLOAD_FOLDER']))

class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


db.create_all()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        # flash('No file part')
        # return redirect(request.url)
        return jsonify({'msg': 'No file part'}), 400
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        # flash('No selected file')
        # return redirect(request.url)
        return jsonify({'msg': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        # filename = secure_filename(file.filename)
        suffix = "images.jpg"
        ident = uuid4().__str__()[:8]
        filename = f"{ident}-{suffix}"
        filepath = app.config['UPLOAD_FOLDER'] + "/" + filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        upload = Upload(file=filepath)
        db.session.add(upload)
        db.session.commit()
        # return redirect(url_for('download_file', name=filename))
        return jsonify({'msg': 'Successfully'}), 200
