from flask import Flask, render_template, url_for, flash, request, redirect
import jinja2
import sqlite3
import re  # To validate email addresses: https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/

app = Flask(__name__)
app.secret_key = "8635c8244367b3954287e06f"  # Secret key from test.py
conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS emails
             (id INTEGER PRIMARY KEY, email text NOT NULL)''')
             #AUTOINCREMENT is to prevent the reuse of ROWIDs from previously deleted rows.


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/articles')
def articles():
    return render_template("articles.html")

@app.route('/beliefs')
def beliefs():
    return render_template("beliefs.html")

@app.route('/contact', methods=['POST', 'GET'])
def contact():
    error = None
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        if request.method == 'GET':
            return render_template("contact.html")
        elif request.method == 'POST':
            inserted_email = request.form.get('email')  # To make the rest of the code cleaner
            print(inserted_email)

            if not inserted_email:
                error = 'Please enter an email address!'
            else:
                test = cur.execute("SELECT email from emails WHERE email=:input", {"input": inserted_email})
                test = cur.fetchall()  # Without fetchall it returned an object 
                if len(test) == 0:
                    cur.execute("INSERT INTO emails (id, email) VALUES (NULL, '{}')".format(inserted_email))
                    con.commit()
                    flash('You were successfully registered!', 'info')
                    return redirect(url_for('home'))
                else: 
                    error = 'This email address has already been taken. Please register with a different email.'
        return render_template('contact.html', error=error)


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
