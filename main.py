from flask import Flask, render_template, request, redirect

app = Flask(__name__, template_folder='templates')

items = []  # This list will store the items


@app.route('/')
def index():
    return render_template('index.html', items=items)


@app.route('/create', methods=['POST'])
def create():
    name = request.form['name']
    items.append(name)
    return redirect('/')


@app.route('/update', methods=['POST'])
def update():
    old_name = request.form['old_name']
    new_name = request.form['new_name']
    if old_name in items:
        index = items.index(old_name)
        items[index] = new_name
    return redirect('/')


@app.route('/delete', methods=['POST'])
def delete():
    name = request.form['name']
    if name in items:
        items.remove(name)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
