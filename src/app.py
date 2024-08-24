import os
from flask import Flask, render_template, redirect, url_for, request
import couchdb

app = Flask(__name__, template_folder='../public')

# CouchDB configuration
couchdb_url = os.environ.get('COUCHDB_URL', 'http://admin:qhadmin@localhost:5984/')
couch = couchdb.Server(couchdb_url)

# Create or connect to a database
db_name = os.environ.get('COUCHDB_DB', 'abhi2')
if db_name in couch:
    db = couch[db_name]
else:
    db = couch.create(db_name)

@app.route('/')
def home():
    return redirect(url_for('signin'))

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Example of storing user credentials in CouchDB (you should hash passwords in a real app)
        db.save({'email': email, 'password': password})
        return redirect(url_for('home_page'))
    return render_template('signin.html')

@app.route('/home')
def home_page():
    return render_template('home.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)