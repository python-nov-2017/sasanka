from flask import Flask, flash,request,redirect,session,render_template
from mysqlconnection import MySQLConnector
import re
from flask_bcrypt import Bcrypt
app = Flask(__name__)
bcrypt = Bcrypt(app)
mysql = MySQLConnector(app,'loginreg')
app.secret_key = "secretKey"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

@app.route('/')
def index():
    if "id" in session.keys():
        return redirect('/success')
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    errors = []
    valid = True

    if len(first_name) < 2 or first_name == "":
        flash ("first name cannot be empty and must have more than 2 characters")
        valid = False

    if len(last_name) < 2 or last_name == "":
        flash ("last name cannot be empty and must have more than 2 characters")
        valid = False

    if email == "":
        flash ("email cannot be empty")
    elif not EMAIL_REGEX.match(email):
        flash("email cannot be empty and should be a valid one")
        valid = False
    if username == "" or len(username) < 2:
        flash ("user name cannot be empty and must have more than 2 characters")
        valid = False

    if password =="":
        flash("password cannot be empty - please set a password")
        valid = False
    elif confirm_password != password:
        flash("please enter the correct password twice")
        valid = False
    if valid == True:
        password = bcrypt.generate_password_hash(password)
        query = """INSERT INTO loginreg (first_name, last_name, email, username, password, created_at, updated_at)
                                VALUES (:first_name, :last_name, :email, :username, :password, NOW(), NOW() ) """
        data = {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'username': username,
                'password': password,
                }
        mysql.query_db(query, data)
        flash ("success")
        return redirect('/')

    elif valid == False:
        return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    query = "SELECT * FROM loginreg WHERE username =:username"
    data = {
            'username':username
    }
    user = mysql.query_db(query,data)
    print user[0]
    if len(user) == 0:
        flash("please enter the valid username")
        return redirect('/')
    else:
        user = user[0]
        if bcrypt.check_password_hash(user['password'], password):
            flash ("logging in")
            session["id"] = user["id"]
            return redirect('/success')
        else:
            flash("invalid password")
            return redirect('/')
    return "hit login route"

@app.route('/success')
def success():
    query = "SELECT username FROM loginreg where id =:id"
    data = {
            "id":session['id']
    }
    logged_user = mysql.query_db(query, data)[0]
    return logged_user["username"]

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

app.run(debug=True)
