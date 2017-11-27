from flask import Flask, render_template, request, redirect, flash, session
from mysqlconnection import MySQLConnector
import re
app = Flask(__name__)
mysql = MySQLConnector(app,'email')
app.secret_key = "secretKey"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/success')
def display():
    query = "SELECT id, email, created_at FROM email"
    emails = mysql.query_db(query)
    print emails
    return render_template('success.html',all_emails=emails)

@app.route('/add', methods = ['POST'])
def add():
    if len(request.form['email']) < 1:
        flash ("PLease Enter an email address")
    elif not EMAIL_REGEX.match(request.form['email']):
        flash ('PLease enter a valid email address')
    else:
        query = "INSERT INTO email (email, created_at, updated_at) VALUES (:email, NOW(), NOW())"
        data = {'email': request.form['email']}
        mysql.query_db(query,data)
        flash ("Thanks for entering the email {}".format(data['email']))
        # print email['email']
        return redirect ('/success')
    return redirect('/')




app.run(debug=True)
