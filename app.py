import bcrypt
from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
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
class SignUpFrom(FlaskForm):
    email = EmailField(validators=[InputRequired(), Length(
        min=5, max=50)], render_kw={"placeholder": "Email"})
    password = PasswordField(validators=[InputRequired(), Length(
        min=5, max=20)], render_kw={"placeholder":"Password"})
    username = StringField(validators=[InputRequired(), Length(
        min=5, max=20)], render_kw={"placeholder","username"})
    age = IntegerField(validators=[InputRequired(), Length(
        min=2, max=2)], render_kw={"placeholder", "age"})
    gender = StringField(validators=[InputRequired(), Length(
        min=4, max=30)], render_kw={"placeholder","gender"})
    location = StringField(validators=[InputRequired(), Length(
        min=4, max=50)], render_kw={"placeholder","location"})
    
    submit = SubmitField("Register")

    #validating the email to make sure that one email has
    #only one account
    def validate_email(self, email):
        existing_email = User.query.filter_by(
            email=email.data).first()
        if existing_email:
            raise ValidationError("This email already exists.")

#creating the login form
class LoginFrom(FlaskForm):
    email = EmailField(validators=[InputRequired(), Length(
        min=5, max=50)], render_kw={"placeholder": "Email"})
    password = PasswordField(validators=[InputRequired(), Length(
        min=5, max=20)], render_kw={"placeholder":"Password"})
    submit = SubmitField("Login")



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginFrom()
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpFrom()

    #have a look at location to upgrade it
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data)
        new_user = User(email=form.email.data, password=hashed_pw,
        username=form.username.data, age=form.age.data, 
        gender=form.gender.data, location=form.location.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect('index.html', form=form)

    return render_template('signup.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)
