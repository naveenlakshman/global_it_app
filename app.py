
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']
        mobile = request.form['mobile']
        admission_date = request.form['admission_date']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name, email, course, mobile, admission_date) VALUES (?, ?, ?, ?, ?)",
                       (name, email, course, mobile, admission_date))
        conn.commit()
        conn.close()

        return redirect(url_for('students'))

    return render_template('register.html')

@app.route('/students')
def students():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    conn.close()
    return render_template('students.html', students=rows)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('students'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']
        mobile = request.form['mobile']
        admission_date = request.form['admission_date']

        cursor.execute("UPDATE students SET name = ?, email = ?, course = ?, mobile = ?, admission_date = ? WHERE id = ?",
                       (name, email, course, mobile, admission_date, id))
        conn.commit()
        conn.close()
        return redirect(url_for('students'))

    cursor.execute("SELECT * FROM students WHERE id = ?", (id,))
    student = cursor.fetchone()
    conn.close()
    return render_template('edit.html', student=student)

if __name__ == '__main__':
    app.run(debug=True)
