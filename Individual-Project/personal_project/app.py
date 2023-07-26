from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates')



config = {
  "apiKey": "AIzaSyB1mZFyqwgnSmWm9mkaq3WoWk7Pucf3Kbg",
  "authDomain": "personal-project-70330.firebaseapp.com",
  "projectId": "personal-project-70330",
  "storageBucket": "personal-project-70330.appspot.com",
  "messagingSenderId": "424222857230",
  "appId": "1:424222857230:web:732167c2af12cfb37c045f",
  "measurementId": "G-N3KCX4CXFL",
  "databaseURL":"https://personal-project-70330-default-rtdb.europe-west1.firebasedatabase.app/"
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'
  
  
@app.route('/', methods=['GET', 'POST'])
def signin():
    
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('home'))
        except:
            error = "AUTH FAILED"
            return render_template("signin.html", error = error)
    else:
        return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        bio = request.form['bio']
        username = request.form['username']
        fullname= request.form['fullname']


        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            UID = login_session['user']['localId']
            user = {"bio":bio,"username":username,"name":fullname,"email":email}
            db.child('USERS').child(UID).set(user)
            return render_template("signin.html")
        except: 
            return render_template("signup.html")
    else:
        return render_template("signup.html")




@app.route('/home', methods=['POST', 'GET'])
def home():

    

    

    return render_template('home.html')
@app.route('/book_rank', methods=['POST', 'GET'])
def book_rank():
    title = request.form['title']
    desc = request.form['desc']
    book = {"title":title, "desc":desc}
    db.child("BOOKS").push(book)
    
if __name__ == '__main__':
    app.debug = True
    app.run()

