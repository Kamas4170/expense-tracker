from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

DATA_FILE = 'data.json'

def load_expenses():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_expense(expense):
    expenses = load_expenses()
    expenses.append(expense)
    with open(DATA_FILE, 'w') as f:
        json.dump(expenses, f)

@app.route('/', methods=['GET', 'POST'])
def index():
    expenses = load_expenses()
    if request.method == 'POST':
        item = request.form['item']
        amount = request.form['amount']
        save_expense({'item': item, 'amount': amount})
        return redirect('/')
    return render_template('index.html', expenses=expenses)

@app.route('/delete/<int:index>', methods=['POST'])
def delete(index):
    expenses = load_expenses()
    if 0 <= index < len(expenses):
        expenses.pop(index)
        with open(DATA_FILE, 'w') as f:
            json.dump(expenses, f)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
