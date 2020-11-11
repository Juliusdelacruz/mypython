from flask import Flask, request, session, jsonify
from flask_pymongo import PyMongo
from datetime import datetime
app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'apiusers'
app.config['MONGO_URI'] = 'mongodb://192.168.1.10:5000/apiusers'

mongo = PyMongo(app)

@app.route('/')
def index():
    if 'username' in session:
        return 'You are logged in as ' + session['username']
    return 'please login'
    

@app.route('/api/users/login', methods=['POST'])
def login():
    email1 = request.json.get('email')
    password1 = request.json.get('password')
    users = mongo.db.users
    login_user = users.find_one({'email' : email1})

    if login_user:
        if login_user['password'] == password1:
           session['email'] = email1
           lastlogin = login_user['lastlogin']
           now = datetime.now() 
           date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
           users.find_one_and_update({'email' : email1},{"$set": {'lastlogin': date_time}})
           return 'You are logged in as ' + session['email'] + ' last login:' + lastlogin
    return 'Invalid Email or password'

@app.route('/api/users/logout', methods = ['GET'])    
def logout():
    session.clear()
    return 'No current login user'
      
@app.route('/api/users', methods=['GET'])
def get_all_user():
    if 'email' in session:
        users = mongo.db.users
        output = []
        for s in users.find():
          output.append({'name' : s['name'], 'password' : s['password'], 'email' : s['email'], 'lastlogin' : s['lastlogin']})
        return jsonify(output)  
    return 'Please login'
    
    
@app.route('/api/users/newuser', methods = ['POST'])
def new_user():
    if 'email' in session:
        if request.method == 'POST':
           name1 = request.json.get('name')
           password1 = request.json.get('password')
           email1 = request.json.get('email')
           users = mongo.db.users
           existing_user = users.find_one({'email' : email1})

           if existing_user is None:
               users.insert({'name': name1, 'password': password1, 'email': email1, 'lastlogin': '1'})
               return 'User created ' + name1 + ' ' + email1
           return 'Email already in use!' 
        return
    return 'Please login'

@app.route('/api/users/deleteuser', methods = ['POST'])
def delete_user():
    if 'email' in session:
        if request.method == 'POST':
           email1 = request.json.get('email')
           users = mongo.db.users
           existing_user = users.find_one({'email' : email1})
           if existing_user is not None:
               users.remove({'email': email1})
               return 'user deleted' + email1 
           return 'Email not registered' 
        return
    return 'Please login'
    
@app.route('/api/users/changepassword', methods = ['POST'])
def update_user():
    if 'email' in session:
        if request.method == 'POST':
           email1 = request.json.get('email')
           newpassword = request.json.get('newpassword')
           users = mongo.db.users
           existing_user = users.find_one({'email' : email1})
           if existing_user is not None:
               users.find_one_and_update({'email' : email1},{"$set": {'password': newpassword}})
               return 'password change for user:' + email1 
           return 'Email not registered' 
        return
    return 'Please login'

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)