from flask import Flask, render_template, request, redricict, url_for, flash
import random
import sqlite3
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

def get_db_connection():
    conn = sqlite3.connect('yatchs.html')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    with app.open_resource('schema.sql') as f:
        conn.executescript(f.read().decode('uft8'))
    conn.close()
@app.route('/new',methods=('POST','GET'))
def New_Yatch():
    if request.method == 'POST':
        yatch_name = request.form['yatch_name']
        manufacturer = request.form['manufacturer']
        model = request.form['model']
        year_manufacture = request.form['year_manufacture']
        length = request.form['length']
        price = request.form['price']

        if not yatch_name or not manufacturer or not model or not year_manufacture or not length or not price:
            flash('all fields requied')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO yatchs (')
            conn.
