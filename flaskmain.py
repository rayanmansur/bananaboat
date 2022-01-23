from flask_socketio import SocketIO
from enum import unique
from flask import Flask, render_template, flash, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

app = Flask(__name__)

# Add Database
# OLD SQLite DB
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# New MYSQL db

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost/our_users'

# Secret Key!
app.config['SECRET_KEY'] = "penis"

socketio = SocketIO(app)
socketio.run(app, debug=True)
#Initialize the database
db = SQLAlchemy(app)

logInManager = LoginManager()
logInManager.init_app(app)
logInManager.login_view = 'login'

@logInManager.user_loader
def loadUser(userId):
    return Users.query.get(int(userId))


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)

    email = db.Column(db.String(200), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    # password_hash = db.Column(db.String(128))

    # @property
    # def password(self):
    #     raise AttributeError('password is not a readable attribute')

    
    # @password.setter
    # def



    # Create a string
    def __repr__(self):
        return '<Username %r' %self.username


class passwordForm(FlaskForm):
    email = EmailField("Enter Email", validators=[DataRequired()])
    password = PasswordField("Enter password", validators=[DataRequired()])
    register = SubmitField("Register")

#Create a Form Class
class registerForm(FlaskForm):
    username = StringField("Enter Username", validators=[DataRequired()])
    email = EmailField("Enter Email", validators=[DataRequired()])
    password = PasswordField("Enter password", validators=[DataRequired()])
    register = SubmitField("Register")

class logInForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    login = SubmitField("Login")


@app.route('/')

def index():
    return render_template("index.html")

# # Update Database Record
# @app.route('/delete/<int:id>')
# def delete(id):
#     usernameToDelete = Users.query.get_or_404(id)
#     username = None
#     password = None
#     email = None
#     form = registerForm()
    

#     try:
#         db.session.delete(usernameToDelete)
#         db.session.commit()

        
#         our_users = Users.query.order_by(Users.date_added)
#         return redirect("../register", code=302) 
#         #render_template("registerscreen.html",
#         #username=username, password=password, email=email, form=form, our_users=our_users)
#     except:
#         print("GOSH TOOTIN DARN DJFKLAJDSJFAJLKF")
        
@app.route('/testPw', methods=['GET', 'POST'])
def testPw():
    email = None
    password = None
    passwordToCheck = None
    passed = None
    form = passwordForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        form.email.data = ''
        form.password.data = ''

        # Look up user by email
        passwordToCheck = Users.query.filter_by(email=email).first()

        # Check passwords work
        print(passwordToCheck.password, password)
        if passwordToCheck.password == password:
            passed = True
        else:
            passed = False
        print(passed)
        


    return render_template('testPw.html', form=form, email=email, password=password, passwordToCheck=passwordToCheck, passed=passed)


@app.route('/register', methods=['GET', 'POST'])
# registration page
def register():
    if current_user.is_authenticated == False:
        print("11111111111111")
        username = None
        email = None
        password = None
        form = registerForm()
        print("22222222222222")
        # Validate Form
        if form.validate_on_submit():
            print("3333333333333333333")
            user = Users.query.filter_by(email=form.email.data).first()
            print("4444444444444444")
            if user is None:
                print("Fffffffffffffuck")
                user = Users(username=form.username.data, email=form.email.data, password=form.password.data)
                print("nice")
                db.session.add(user)
                db.session.commit()
                username = form.username.data
                # password = form.password.data
                email = form.email.data
                form.username.data = ''
                form.password.data = ''
                form.email.data = ''
                our_users = Users.query.order_by(Users.date_added)
                return render_template("registerscreen.html",
                username=username, password=password, email=email,
                form=form, our_users=our_users)

                flash("User Added Successfully")
            else:
                flash("This email already exists")
                form.username.data = ''
                form.password.data = ''
                form.email.data = ''
            
            
            

        our_users = Users.query.order_by(Users.date_added)
        return render_template("registerscreen.html",
        username=username, password=password, email=email,
        form=form, our_users=our_users)
    else:
        return redirect(url_for('search'))

# @app.route('/user/<id>')
# # user settings page
# def user(id):
#     #gets id from url and saves it as userId to be used in user.html page
#     return render_template("user.html", userId=id)

@app.route('/web')
def web():
    return render_template("web.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated == False:
        form = logInForm()
        if form.validate_on_submit():
            user = Users.query.filter_by(email=form.email.data).first()
            if user:
                # Check passwords
                print(user.password, form.password.data)
                if user.password == form.password.data:
                    login_user(user)
                    return redirect(url_for('user'))
                else:
                    flash("Wrong Password - Try Again!")
            else:
                flash("This Email Doesn't Exist")

        return render_template('login.html', form=form)
    else:
        return redirect(url_for('search'))


@app.route('/user', methods=['GET', 'POST'])
@login_required
def user():
    return render_template('user.html')

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("Logged out")
    return redirect(url_for('login'))

@app.route('/search')
@login_required
def search():
    return render_template('search.html')

@app.route('/videochat')
def videochat():
    return render_template('videochat.html')

@app.route('/csgo')
def csgo():
    return render_template('csgo.html')

@app.route('/valorant')
def valorant():
    return render_template('valorant.html')

@app.route('/csgolobby/<id>')
def csgolobby(id):
    return render_template('csgolobby.html', id=id)

# def messageReceived(methods=['GET', 'POST']):
#     print('message was received!!!')

# @socketio.on('my event')
# def handle_my_custom_event(json, methods=['GET', 'POST']):
#     print('received my event: ' + str(json))
#     socketio.emit('my response', json, callback=messageReceived)



@app.route('/valorantlobby/<id>')
def valorantlobby(id):
    return render_template('valorantlobby.html', id=id)
