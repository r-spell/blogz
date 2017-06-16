from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:blogit@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)

    def __init__(self, title):
        self.title = title
        self.body = ''

def get_bloglist():
    return Blog.query.all()

def empty_string(string):
    if len(string)==0:
        return True
    return False

@app.route('/')
def index():
    blogs = get_bloglist

    return render_template('index.html',page_title="Build a Blog", 
        blogs=blogs)




@app.route('/newpost')
def new_post():
    return render_template('newpost.html',page_title="Add a Blog Entry")


@app.route('/newpost', methods=['POST'])
def submit_post(): 
    title= request.form['title']
    blog = Blog(title)
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

    
    # show blog page  and commit if no errors
    if not empty_string(body_text) and not empty_string(title):
        db.session.commit() 
        return redirect('/')
    # show errors on new post page if any errors
    else: 
        return render_template('newpost.html',title_error=title_error,body_error=body_error,page_title="Add a Blog Entry")

if __name__ == '__main__':
    app.run()