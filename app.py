#importing the necessary packages and libraries for the app
from flask import Flask, render_template, url_for, redirect, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from datetime import datetime



#creating the app and database
#creating bcrypt to hash the password
app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = 'secretkey'

#creating the login manager
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

#home page / reception page
@app.route('/')
def index():
    return render_template('index.html')

#Signup page to collect data to create a user profile
@app.route('/signup', methods=['GET', 'POST'])
def signup():

    #getting the data from the form in the fronend through post request
    if request.method == 'POST':
        first_name = request.form['fname']
        last_name = request.form['lname']
        email = request.form['mail']
        password = request.form['pwd']
        password2 = request.form['pwd2']
        age = request.form['age']
        gender = request.form['gender']
        location = request.form['location']

        #validating the data before pushing them to database to create a user profile
        if len(first_name) > 50:
            flash('First name must be less than 50 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 2 characters.', category='error')
        elif len(last_name) > 50:
            flash('Last name must be less than 50 characters.', category='error')
        elif len(last_name) < 2:
            flash('Last name must be greater than 2 characters.', category='error')
        elif len(email) > 50: 
            flash('Email must be less than 50 characters.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif password != password2:
            flash('Passwords do NOT match', category='error')
        elif len(password) < 8:
            flash('Password must be at least 8 characters', category='error')
        elif age == "":
            flash('Age must be filled', category='error')
        elif gender == "":
            flash('Gender must be filled', category='error')
        elif location == "":
            flash('Location must be filled', category='error')
        else:
            #checking if the email is used already
            existing_email = User.query.filter_by(
                    email=email).first()
            if existing_email:
                flash("This email already exists.", category='error')
                return redirect(url_for('signup'))

            #if email does not exist hashing the pw and creating the user profile
            else:    
                hashed_pw = bcrypt.generate_password_hash(password)

                new_user = User(email=email, first_name=first_name, 
                password = hashed_pw ,last_name=last_name, age=age, 
                gender=gender, location=location)
            
                db.session.add(new_user)
                db.session.commit()
                flash('Account created!', category='success')
                return redirect(url_for('index'))

        flash('Account not created!', category='error')
        return redirect(url_for('signup'))
    #if the request is get, just showing the template to the user           
    else:
        return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form['mail']
        password = request.form['pwd']
        user = User.query.filter_by(email=email).first()

        if email == '':
            flash('Please enter your Email', category='error')
        elif password == '':
            flash('Please enter your Password', category='error')
        else:
            if user:
                if bcrypt.check_password_hash(user.password, password):
                    login_user(user)
                    flash('Successfully signed in', category='success')
                    return redirect(url_for('profile'))
                else:
                    flash('Incorrect Email or Password', category='error')
                    return redirect(url_for('login'))

            else:
                flash("This user does not exist", category='error')
                return redirect(url_for('login'))

        return redirect(url_for('login'))
        
    else:
        return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/ads', methods=['GET'])
# @login_required
def ads():
    buttonValue = ""

    if request.args.get('filter'):

        if request.args.get('filter') == 'Asc':
            
            buttonValue = "Ascending"    
            posts = Post.query.order_by(Post.date_created.asc()).all() 
            
            return render_template(
                'ads.html', 
                posts=posts,
                buttonValue=buttonValue)

        elif request.args.get('filter') == 'Desc':
            
            buttonValue = "Descending"
            posts = Post.query.order_by(Post.date_created.desc()).all() 
            
            return render_template(
                'ads.html', 
                posts=posts,
                buttonValue=buttonValue)

    else:

        posts = Post.query.order_by(Post.date_created).all() 
        
        return render_template(
            'ads.html', 
            posts=posts,
            buttonValue=buttonValue)


@app.route('/search', methods=['GET'])
def search():

    search = request.args.get('search')
    result = db.session.query(Post, User).join(User). \
        filter(User.first_name.ilike(f'%{search}%')).all()
            
    return render_template(
        'search.html', 
        result=result,
        search=search)


@app.route('/profile', methods=['GET', 'POST'])
# @login_required
def profile():

    if request.method == 'POST':
        content = request.form['content']

        if len(content) < 1:
            flash("Task too short!", category='error')
            
        else:
            new_post = Post(
                content=content, 
                user_id=current_user.id)
        
            db.session.add(new_post)
            db.session.commit()
            flash("Task created successfully", category='success')
            return redirect('ads')
        
        return redirect(url_for('profile'))

    else:
        return render_template(
            'profile.html', 
            user=current_user)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    posts = Post.query.get_or_404(id)

    if request.method == 'POST':

        if request.form['content'].strip() == '':
            flash('Post cannot be blank', category='error')
            return redirect(url_for('profile'))

        elif len(request.form['content']) > 0:
            posts.content = request.form['content']
            db.session.commit()
            flash('Post edited', category='success')
            return redirect(url_for('profile'))

        else:
            flash('Post cannot be blank', category='error')
            return redirect(url_for('profile'))

    else:
        return render_template(
            'update.html', 
            posts=posts)


@app.route('/delete/<int:id>')
@login_required
def delete(id):
    posts_to_delete = Post.query.get_or_404(id)

    if posts_to_delete:
        db.session.delete(posts_to_delete)
        db.session.commit()
        flash('Post deleted', category='success')
        return redirect(url_for('profile'))

    else:
        flash("Post not exist", category='error')
        return redirect(url_for('profile'))

if __name__ == "__main__":
    app.run(debug=True)
