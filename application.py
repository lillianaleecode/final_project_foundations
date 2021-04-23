from flask_wtf import FlaskForm
from flask_wtf import Form
from flask import Flask, render_template, url_for, redirect, flash, request, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
#for the form:
from forms import RegistrationForm, LoginForm, ContactForm
from wtforms import StringField, SubmitField, TextField, TextAreaField, SubmitField
from flask_wtf import Form


app = Flask(__name__)

#for removing FSADeprecationWarning
SQLALCHEMY_TRACK_MODIFICATIONS = False


#for the form:
app.config["SECRET_KEY"] = '79537d00f4834892986f09a100aa1edf'

#part 4, doing the database
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql:///lartl@LAPTOP-2MQ85RDV:''@localhost/database'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= False
app.permanent_session_lifetime = timedelta(minutes=5)

#for initializing the database
db = SQLAlchemy(app)

#database for to do list
class Todolist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200),nullable=False)
    completed = db.Column(db. Integer, default=0)
    data_created = db.Column(db.DateTime, default=datetime.utcnow)

    #create a function to return a string when  we add
    def __repr__(self):
        return '<Task %r>' % self.id

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True,nullable=False)
  email = db.Column(db.String(120), unique=True,nullable=False)
  image_file = db.Column(db.String(20), unique=True,nullable=False, default='default.jpg')
  password = db.Column(db.String(60),nullable=False)
  #posts = db.relationship('Post', backref='author', lazy=True)

  #def __init__(self, username, email, password):
    #self.username = username
    #self.email = email
    

def __repr__(self):
  return f"User('{self.username}', '{self.email}')"
  return f"User('{self.username}', '{self.email}', '{self.image_file}')"



class Post(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   title = db.Column(db.String(100), nullable=False)
   data_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
   content = db.Column(db.Text, nullable=False)
   user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

def __repr__(self):
  return f"Post('{self.title}','{self.date_posted}')"


posts= [
  {
      'author':'Lilli',
      'title':'Blog 1',
      'content': 'this is my first blog!',
      'date_posted': 'April 20th, 2020',
  },
    {
      'author':'Lee',
      'title':'Blog 2',
      'content': 'this is my second blog!',
      'date_posted': 'April 21th, 2020',
  },

]


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
    flash(f'Account created for {form.username.data}!', 'success')
    return redirect(url_for('home'))
  return render_template('register.html', title= 'Register', form=form)

#for the form:
@app.route('/login', methods=["GET", "POST"])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    if form.email.data == 'admin@blog.com' and form.password.data == '123':
      flash('you have been logged in', 'success')
      return redirect(url_for('home'))
    else:
      flash('log in unsucessful, please check username and password','danger')
  return render_template('login.html', title= 'Login', form=form)

 #form log in intento 2
#@app.route('/login', methods=["GET", "POST"])
#def login():
 # form = LoginForm()
  #if request.method =='POST':
   # session.permanent = True
    #user = request.form["nm"]
    #session["user"] = user

    #found_user = User.query.filter_by(name=user).first()
    #if found_user:
     # session["email"] = found_user.email
    #else:
     # usr = user(user, "")
      #db.session.add(usr)
      #db.session.commit()
    
    #flash("Login Succesful!")
    #return redirect(url_for("user"))
  #else:
   #  if "user" in session:
    #   flash("Alreadyd Logged in!")
     #  return redirect(url_for("user"))
     #return render_template("login.html", title= 'Login', form=form)  


#for the form:
#@app.route('/contact')
#def contact():
  #form = ContactForm()
 # return render_template ('contact.html', title= 'Contact', form=form)

#extra page just in case, not working
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


if __name__ == '__main__': #this piece of code let us run with calling out "python xxx.py" in the terminal, instead of running with "flask run"
    #db.create_all() #database
    app.run( debug = True)
   #debug true help us refresh the code everytime we save changes.
    
