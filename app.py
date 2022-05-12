import bcrypt
from flask import Flask, render_template, url_for, redirect, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
# from requests import request
from flask_bcrypt import Bcrypt
from datetime import datetime


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

#creating user table in the database
#and creating posts attribute to link
#the child table with the parent
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(30), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    posts = db.relationship('Post', backref='user')

    #creating this representative function 
    #if there is an error i will be able to
    #see the user the error coming from
    def __repr__(self):
        return f'<User {self.id}>'

#creating post table in the database
#and creating the user_id to link this table
#with the parent
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(400), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    #creating this representative function 
    #if there is an error i will be able to
    #see the post the error coming from
    def __repr__(self):
        return f'<Post {self.id}>'


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':
        first_name = request.form['fname']
        last_name = request.form['lname']
        email = request.form['mail']
        password = request.form['pwd']
        age = request.form['age']
        gender = request.form['gender']
        location = request.form['location']

        hashed_pw = bcrypt.generate_password_hash(password)

        new_user = User(email=email, first_name=first_name, 
        password = hashed_pw ,last_name=last_name, age=age, 
        gender=gender, location=location)
     
        existing_email = User.query.filter_by(
                email=email).first()
        if existing_email:
            flash("This email already exists.")

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('index'))

        except:
            return 'Something went wrong'
            
    else:
        return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form['mail']
        password = request.form['pwd']
        user = User.query.filter_by(email=email).first()
        
        if user:
            if bcrypt.check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('ads'))

        else:
            raise flash("This email already exists.")

    else:
        return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/ads', methods=['GET', 'POST'])
# @login_required
def ads():

    posts = Post.query.order_by(Post.date_created).all()
    return render_template('ads.html', posts=posts)



@app.route('/post', methods=['GET', 'POST'])
@login_required
def post():

    if request.method == 'POST':
        content = request.form['content']
        new_post = Post(content=content)

        try:
            db.session.add(new_post)
            db.session.commit()
            return redirect('ads')
        
        except:
            return 'Something went wrong'

    else:
        posts = Post.query.order_by(Post.date_created).all()
        return render_template('post.html', posts=posts)


if __name__ == "__main__":
    app.run(debug=True)
