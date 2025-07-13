from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'globalit@2025'  # Keep this secret in real apps


# ---------- Utility Function ----------
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


# ---------- Routes ----------

@app.route('/')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == '1234':
            session['logged_in'] = True
            return redirect(url_for('register'))  # ✅ redirect to register
        else:
            return "Invalid credentials"

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']
        mobile = request.form['mobile']
        admission_date = request.form['admission_date']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name, email, course, mobile, admission_date) VALUES (?, ?, ?, ?, ?)",
                       (name, email, course, mobile, admission_date))
        conn.commit()
        conn.close()

        return redirect(url_for('students'))

    return render_template('register.html')


@app.route('/students')
def students():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students').fetchall()
    conn.close()
    return render_template('students.html', students=students)


@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    conn = get_db_connection()
    conn.execute("DELETE FROM students WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('students'))


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']
        mobile = request.form['mobile']
        admission_date = request.form['admission_date']

        cursor.execute("""
            UPDATE students SET name = ?, email = ?, course = ?, mobile = ?, admission_date = ?
            WHERE id = ?
        """, (name, email, course, mobile, admission_date, id))
        conn.commit()
        conn.close()
        return redirect(url_for('students'))

    cursor.execute("SELECT * FROM students WHERE id = ?", (id,))
    student = cursor.fetchone()
    conn.close()
    return render_template('edit.html', student=student)


# ---------- Run App ----------
if __name__ == '__main__':
    app.run(debug=True)
