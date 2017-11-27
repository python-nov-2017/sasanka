from flask import Flask, flash,request,redirect,session,render_template
from mysqlconnection import MySQLConnector
import re
app = Flask(__name__)
mysql = MySQLConnector(app,'fullfriends')
app.secret_key = "secretKey"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

@app.route("/")
def index():
    friends = mysql.query_db("SELECT * FROM fullfriends")
    return render_template ('index.html', all_friends=friends)

@app.route('/friends', methods=['POST'])
def create():
    if len(request.form['first_name']) < 1 or len(request.form['last_name']) < 1 or len(request.form['email']) < 1:
        flash("Please enter the information in the Fields")
    elif not EMAIL_REGEX.match(request.form['email']):
        flash("Please enter a valid email address")
    else:
        query = "INSERT INTO fullfriends (first_name, last_name, email, created_at, updated_at) VALUES (:first_name,:last_name, :email, NOW(), NOW())"
        data = {'first_name': request.form['first_name'],
                'last_name': request.form['last_name'],
                'email': request.form['email']
                }
        mysql.query_db(query,data)
        flash ("Success friend has been added")
    return redirect ('/')

@app.route('/friends/<id>/edit')
def edit(id):
    query = "SELECT * FROM fullfriends WHERE id=:id"
    data = {
        'id': id
    }
    friends = mysql.query_db(query, data)[0]
    return render_template('edit.html', all_friends=friends)

@app.route('/friends/<id>', methods=['POST'])
def update(id):
    if len(request.form['first_name']) < 1 or len(request.form['last_name']) < 1 or len(request.form['email']) < 1:
        flash("Please enter the information in the Fields")
    elif not EMAIL_REGEX.match(request.form['email']):
        flash("Please enter a valid email address")
    else:
    	query = "UPDATE fullfriends SET first_name = :first_name, last_name = :last_name, email = :email WHERE id = :id"
    	data = {
    			'first_name': request.form['first_name'],
    			'last_name': request.form['last_name'],
    			'email': request.form['email'],
    			'id': id
    	}
    	mysql.query_db(query, data)
        return redirect ('/')
    # url = '/friends/{}'.format(id)
    # print url
    return redirect ('/friends/{}/edit'.format(id))



@app.route('/friends/<id>/delete', methods=['POST'])
def destroy(id):
	 query = "DELETE FROM fullfriends WHERE id = :id"
	 data= {
			'id': id
	 }
	 mysql.query_db(query, data)
	 return redirect('/')

app.run(debug=True)
