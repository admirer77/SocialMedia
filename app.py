from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime


app = Flask(__name__)
app.secret_key = 'your_secret_key'


from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://root:21951a6790@db123.zw2gjtz.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


db = client["socialmedia_db"]
posts_collection = db["posts"]
users_collection = db["users"]

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Check if the username already exists in the database (you should implement this check)
        
        users_collection.insert_one({'username': username, 'password': password})
        return "Registerred succesfully"
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = users_collection.find_one({'username': username, 'password': password})
    if user:
        session['username'] = username
        return redirect(url_for('dashboard'))
    return 'Invalid login credentials'


@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        posts = posts_collection.find()
        return render_template('dashboard.html', posts=posts)
    return redirect(url_for('login'))



@app.route('/logout')
def logout():
    session.pop('username', None)
    return "logged out"

@app.route('/post', methods=['GET','POST'])
def post():
    if 'username' in session:
        if request.method == 'POST':
            posted_by = session['username']
            description = request.form['description']
            posted_at = datetime.now()
            posts_collection.insert_one({'posted_by': posted_by, 'description': description,  'posted_at': posted_at})
            return redirect(url_for('dashboard'))
        return render_template('post.html')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)