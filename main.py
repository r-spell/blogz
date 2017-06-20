from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:goblog@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'b33pGcys&zP3B'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __init__(self, title, owner):
        self.title = title
        self.body = ''
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship("Blog", backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

# function gives list of all blog entries
def get_bloglist():
    return Blog.query.all()


# function for testing inputs, returns true if empty string given 
def empty_string(string):
    if len(string)==0:
        return True
    return False

@app.route('/login', methods=['POST','GET'])
def login():
    #check for request type
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        # TODO add further validation
        # TODO  User enters a username that is stored in the database with the correct password and is redirected to the /newpost page with their username being stored in a session.
        #User enters a username that is stored in the database with an incorrect password and is redirected to the /login page with a message that their password is incorrect.
        #User tries to login with a username that is not stored in the database and is redirected to the /login page with a message that this username does not exist.
        #User does not have an account and clicks "Create Account" and is directed to the /signup page
        # user with valid username and password redirected to /newpost, username stored in session
        if user and user.password == password: #if "user" has value "none" (user does not exist) will not meet condition
            session['username'] = username
            # TODO add flash message "Logged in"
            return redirect('/newpost')

    return render_template('login.html')

# shows the newpost page
@app.route('/newpost')
def new_post():
    return render_template('newpost.html',page_title="Add a Blog Entry")


# handles user inputs to newpost page 
@app.route('/newpost', methods=['POST'])
def submit_post(): 
    owner = User.query.filter_by(username=session['username']).first()
    title = request.form['title']
    blog = Blog(title, owner)
    body_text = request.form['body_text'] 
    blog.body = body_text
    body_error = ''
    title_error = ''
    db.session.add(blog)


    # check for errors in inputs and clear if there are errors
    if empty_string(title):
        title_error = "Please fill in the title"

    if empty_string(body_text):
        body_error = "Please fill in the body"

    # show main blog page  and commit if no errors
    if not empty_string(body_text) and not empty_string(title):
        db.session.commit() 
        blog = db.session.query(Blog).order_by(Blog.id.desc()).first()
        blog_id=blog.id
        return redirect('/blog?id='+str(blog_id))
    # show errors on newpost page if any errors
    else: 
        return render_template('newpost.html',title_error=title_error,body_error=body_error,page_title="Add a Blog Entry", title=title, body_text=body_text)


@app.route('/')
def index():
    blogs = get_bloglist()
    return render_template('index.html',page_title="Build a Blog", 
        blogs=blogs)


# display individual blog with "id=" and id number in query string
@app.route('/blog')
def blog_display():
    blog_id = request.args.get('id')
    blog = Blog.query.get(blog_id)
    blog_title = blog.title
    blog_body = blog.body

    return render_template('blog.html',blog_title=blog_title, blog_body=blog_body)


if __name__ == '__main__':
    app.run()