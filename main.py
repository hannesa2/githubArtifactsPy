from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__, template_folder='templates')

items = []  # This list will store the items
UPLOAD_FOLDER = "files"


@app.route('/')
def index():
    items = os.listdir(UPLOAD_FOLDER)
    return render_template('index.html', items=items)


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


if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    items = os.listdir(UPLOAD_FOLDER)
    app.run(debug=True)
