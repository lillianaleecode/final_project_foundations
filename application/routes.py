from flask import Flask, render_template, url_for, redirect, flash, redirect, request
from application import app, db, bcrypt
from application.forms import RegistrationForm, LoginForm, ContactForm
from application.models import User, Post, Todolist
from flask_bcrypt import Bcrypt

#for login
from flask_login import UserMixin, LoginManager
from flask_sqlalchemy import SQLAlchemy


#app = Flask(__name__)

#for removing FSADeprecationWarning
#SQLALCHEMY_TRACK_MODIFICATIONS = False


#for the form:
#app.config["SECRET_KEY"] = '79537d00f4834892986f09a100aa1edf'

#part 4, doing the database
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql:///lartl@LAPTOP-2MQ85RDV:''@localhost/database'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
#app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= False
#app.permanent_session_lifetime = timedelta(minutes=5)

#for initializing the database
#db = SQLAlchemy(app)

#for authentication
bcrypt = Bcrypt(app)

#for Login
login_manager = LoginManager(app)



posts= [
  {
      'author':'Co-authored by Pippa Elliott, MRCVS',
      'title':'How to Take Care of a Cat',
      'content': 'With their playful personalities, affectionate behavior, and adorable faces, cats can be the ideal pet. But, despite popular opinion, cats are not maintenance-free! To keep your cat healthy and happy, you need to know how to take care of and provide the best possible life for your new furry friend.',
      'date_posted': 'Last Updated: April 10, 2021',
  },
    {
      'author':'Stacy Hackett',
      'title':'Cats 101: Basic Health & Care Tips to Keep Your Cat Healthy',
      'content': "How often do you take your cat to the veterinarian? In observance of National Cat Health Month, we want to remind you that even if your cat does not appear to be sick, preventative care is important. Between visits to your cat's veterinarian, here are 10 ways to keep your cat healthy.",
      'date_posted': 'April 21th, 2020',
  },

]


#database for to do list
# class Todolist(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     content = db.Column(db.String(200),nullable=False)
#     completed = db.Column(db. Integer, default=0)
#     data_created = db.Column(db.DateTime, default=datetime.utcnow)

#     #create a function to return a string when  we add
#     def __repr__(self):
#         return '<Task %r>' % self.id

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# class User(db.Model, UserMixin):
#   id = db.Column(db.Integer, primary_key=True)
#   username = db.Column(db.String(20), unique=True,nullable=False)
#   email = db.Column(db.String(120), unique=True,nullable=False)
#   image_file = db.Column(db.String(20), unique=True,nullable=False, default='default.jpg')
#   password = db.Column(db.String(60),nullable=False)
  

# class User(db.Model):
#   id = db.Column(db.Integer, primary_key=True)
#   username = db.Column(db.String(20), unique=True,nullable=False)
#   email = db.Column(db.String(120), unique=True,nullable=False)
#   image_file = db.Column(db.String(20), unique=True,nullable=False, default='default.jpg')
#   password = db.Column(db.String(60),nullable=False)

  #posts = db.relationship('Post', backref='author', lazy=True)

  #def __init__(self, username, email, password):
    #self.username = username
    #self.email = email
    
#   def __repr__(self):
#     return f"User('{self.username}', '{self.email}')"
#     return f"User('{self.username}', '{self.email}', '{self.image_file}')"



# class Post(db.Model):
#   id = db.Column(db.Integer, primary_key=True)
#   title = db.Column(db.String(100), nullable=False)
#   data_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#   content = db.Column(db.Text, nullable=False)
#   user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

#   def __repr__(self):
#     return f"Post('{self.title}','{self.date_posted}')"





@app.route('/home')
@app.route('/')
def home():
    return render_template('home.html', posts=posts, title='Home YEY')

@app.route('/about')
def about():
    return render_template('about.html', posts=posts, title='About Page YEY')

@app.route('/machote')
def machote():
    return render_template('machotelayout.html', title='Machote')    

#for the form:
@app.route('/register', methods=["GET", "POST"])
def register():
  form = RegistrationForm()
  if form.validate_on_submit():
    hashed_password = bcrypt.generate_password_hash(form.password.data)
    user = User(username=form.username.data, email=form.email.data, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    flash('your account has been created, you are now able to log in', 'success')
    return redirect(url_for('login'))
  return render_template('register.html', title= 'Register', form=form)


# # @app.route('/register', methods=["GET", "POST"])
# def register():
#   form = RegistrationForm()
#   if form.validate_on_submit():
#     flash(f'Account created for {form.username.data}!', 'success')
#     return redirect(url_for('home'))
#   return render_template('register.html', title= 'Register', form=form)

#for the form
@app.route('/login', methods=["GET", "POST"])
def login():
  form = LoginForm()
  if form.validate_on_submit():
      user = User.query.filter_by(email=form.email.data).first()
      if user and bcrypt.check_password_hash(user.password, form.password.data):
        login_user(user, remember=form.remember.data)
        return redirect(url_for('home'))
      else:
        flash('log in unsucessful, please check email and password','danger')
  return render_template('login.html', title= 'Login', form=form)


# @app.route('/login', methods=["GET", "POST"])
# def login():
#   form = LoginForm()
#   if form.validate_on_submit():
#     if form.email.data == 'admin@blog.com' and form.password.data == '123':
#       flash('you have been logged in', 'success')
#       return redirect(url_for('home'))
#     else:
#       flash('log in unsucessful, please check username and password','danger')
#   return render_template('login.html', title= 'Login', form=form)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    """Standard `contact` form."""
    form = ContactForm()
    if form.validate_on_submit():
        return redirect(url_for("success"))
    return render_template('contact.html', title= 'Contact', form=form)

#route for to do list post
@app.route('/todolist', methods=['POST','GET'])
def todolist():
    if request.method == 'POST':
        task_content = request.form['content']#if we submit our form, it will give this value, content is from the content form in our index
        new_task = Todolist(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect ('/todolist')
        except:
            return 'there is an issue adding your request'
    else:
        tasks = Todolist.query.order_by(Todolist.data_created).all() #here I created the variable 'tasks'
        return render_template('todolist.html', tasks=tasks)

#route for to do list delete
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todolist.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/todolist')
        
    except:
        return 'there was a problem deleting that task'

#route for to do list update
@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    task = Todolist.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect ('/todolist')

        except: 
            return 'there was an issue updating your task'

    else:
        return render_template('update.html', task=task)
