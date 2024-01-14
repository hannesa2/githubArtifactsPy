from flask import Flask, render_template, request, redirect, flash, url_for, send_from_directory, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
import os

from werkzeug.utils import secure_filename
from passlib.apps import custom_app_context as pwd_context

app = Flask(__name__, template_folder='templates')

UPLOAD_FOLDER = "files"
ALLOWED_EXTENSIONS = {'txt', 'png', 'jpg', 'jpeg', 'gif'}
db = SQLAlchemy(app)
auth = HTTPBasicAuth()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(128))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)


@app.route('/api/users', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400)  # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        abort(400)  # existing user
    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'username': user.username}), 201, {'Location': url_for('get_user', id=user.id, _external=True)}


@app.route('/')
def index():
    return render_template('index.html', items=os.listdir(UPLOAD_FOLDER))


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    print("I do a ", request.method)
    print("---headers---\r\n", request.headers)
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))
    return ''


@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


@app.route('/get', methods=['GET'])
def get():
    name = request.args['name']
    try:
        fp = open(UPLOAD_FOLDER + '/' + name, 'r')
        content = fp.read()
        fp.close()
        return content
    except FileNotFoundError:
        print("Please check the path")


@app.route('/create', methods=['POST'])
def create():
    name = request.form['name']

    fp = open(UPLOAD_FOLDER + '/' + name, 'w')
    fp.write('content of ' + name)
    fp.close()
    return redirect('/')


@app.route('/update', methods=['POST'])
def update():
    old_name = request.form['old_name']
    new_name = request.form['new_name']
    os.rename(UPLOAD_FOLDER + '/' + old_name, UPLOAD_FOLDER + '/' + new_name)
    return redirect('/')


@app.route('/delete', methods=['POST'])
def delete():
    name = request.form['name']
    os.remove(UPLOAD_FOLDER + '/' + name)
    return redirect('/')


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    app.secret_key = 'super secret key'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 200024
    app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    items = os.listdir(UPLOAD_FOLDER)
    app.run(debug=True)
