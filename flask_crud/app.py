from flask import Flask, render_template, request, redirect, url_for, flash
from db import app, mysql  

app.secret_key = "your_secret_key"  

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students")
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', students=data)

@app.route('/add', methods=['POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        cur = mysql.connection.cursor()

        # ✅ Check if email already exists
        cur.execute("SELECT * FROM students WHERE email = %s", (email,))
        existing_student = cur.fetchone()

        if existing_student:
            flash("Error: This email is already registered!")
            cur.close()
            return redirect(url_for('index'))  # Redirect without inserting duplicate

        # ✅ If email is unique, insert new student
        cur.execute("INSERT INTO students (name, email) VALUES (%s, %s)", (name, email))
        mysql.connection.commit()
        cur.close()

        flash("Student added successfully!")
        return redirect(url_for('index'))


@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit_student(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students WHERE id = %s", (id,))
    student = cur.fetchone()
    cur.close()
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE students SET name = %s, email = %s WHERE id = %s", (name, email, id))
        mysql.connection.commit()
        cur.close()
        flash("Student updated successfully!")
        return redirect(url_for('index'))

    return render_template('edit.html', student=student)

@app.route('/delete/<id>')
def delete_student(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM students WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    flash("Student deleted successfully!")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
