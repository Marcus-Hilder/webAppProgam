from flask import Flask, render_template, request, redirect, url_for, flash
import random
import sqlite3
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("home.html")

def get_db_connection():
    conn = sqlite3.connect('Yatchs.db')
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
            conn.execute('INSERT INTO yachts(yatch_name,manufacturer,model,year_manufacture,length,price) VALUES (?,?,?,?,?,?)',(yatch_name, manufacturer, model, year_manufacture, length ,price))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template("new.html")

@app.route('/admin')
def admin():
    conn = get_db_connection()
    sql = "SELECT * FROM yachts;"
    yatch = conn.execute(sql).fetchall()
    conn.close()
    return render_template('view_yatchs.html',yachts=yatch)

@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit_user(id):
    conn = get_db_connection()
    yatch = conn.execute('SELECT * FROM yachts  where id = ?',(id,)).fetchone()
    print(id)
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
            conn.execute('UPDATE yachts SET yatch_name = ?, manufacturer = ?, model = ?, year_manufacture = ?, length = ?, price = ? WHERE id = ?', (yatch_name, manufacturer, model, year_manufacture, length ,price, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('update.html', yatch = yatch)


@app.route('/delete/<int:id>',methods=('POST',))
def  delete_yatchs(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM yachts WHERE id = ?',(id,))
    conn.commit()
    conn.close()
    flash('user deleted successfully')
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True, port=7654)