from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Add Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# Secret Key!
app.config['SECRET_KEY'] = ""
#Initialize the database
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    # Create a string
    def __repr__(self):
        return '<Username %r' %self.username


#Create a Form Class
class registerForm(FlaskForm):
    username = StringField("Enter Username", validators=[DataRequired()])
    password = PasswordField("Enter password", validators=[DataRequired()])
    register = SubmitField("Register")

@app.route('/')

def index():
    return render_template("index.html")

@app.route('/register', methods=['GET', 'POST'])
# registration page
def register():
    username = None
    password = None
    form = registerForm()
    # Validate Form
    if form.validate_on_submit():
        username = form.name.data
        password = form.password.data
        form.username.data = ''
        form.password.data = ''
    return render_template("registerscreen.html", givenUserName = username, givenPassword = password, givenForm = form)

@app.route('/user/<id>')
# user settings page
def user(id):
    #gets id from url and saves it as userId to be used in user.html page
    return render_template("user.html", userId=id)
