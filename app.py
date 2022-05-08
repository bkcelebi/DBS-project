import email
import bcrypt
from flask import Flask, render_template, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, EmailField, StringField, IntegerField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
# from datetime import datetime

#creating the app and database
#creating bcrypt to hash the password
app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = 'secretkey'


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



# class Todo(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     content = db.Column(db.String(200), nullable=False)
#     date_created = db.Column(db.DateTime, default=datetime.utcnow)

#     def __repr__(self):
#         return '<task %r>' % self.id

#creating user table in the database
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(30), nullable=False)
    location = db.Column(db.String(50), nullable=False)

#creating the signup form
class SignUpForm(FlaskForm):
    email = EmailField(validators=[InputRequired(), Length(
        min=5, max=50)], render_kw={"placeholder": "Email"})
    password = PasswordField(validators=[InputRequired(), Length(
        min=5, max=20)], render_kw={"placeholder": "Password"})
    username = StringField(validators=[InputRequired(), Length(
        min=5, max=20)], render_kw={"placeholder": "username"})
    age = IntegerField(validators=[InputRequired()],
        render_kw={"placeholder": "age"})
    gender = StringField(validators=[InputRequired(), Length(
        min=4, max=30)], render_kw={"placeholder": "gender"})
    location = StringField(validators=[InputRequired(), Length(
        min=4, max=50)], render_kw={"placeholder": "location"})
    
    submit = SubmitField("Register")

    #validating the email to make sure that one email has
    #only one account
    def validate_email(self, email):
        existing_email = User.query.filter_by(
            email=email.data).first()
        if existing_email:
            raise ValidationError("This email already exists.")
            #flash("This email already exists.")

#creating the login form
class LoginForm(FlaskForm):
    email = EmailField(validators=[InputRequired(), Length(
        min=5, max=50)], render_kw={"placeholder": "Email"})
    password = PasswordField(validators=[InputRequired(), Length(
        min=5, max=20)], render_kw={"placeholder":"Password"})
    submit = SubmitField("Login")




@app.route('/')
def index():
    form = LoginForm()
    return render_template('index.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()

    #have a look at location to upgrade it
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data)
        new_user = User(email=form.email.data, password=hashed_pw,
        username=form.username.data, age=form.age.data, 
        gender=form.gender.data, location=form.location.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('ads'))
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))



@app.route('/ads', methods=['GET', 'POST'])
# @login_required
def ads():
    return render_template('ads.html')


if __name__ == "__main__":
    app.run(debug=True)
