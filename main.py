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


@app.route('/')
def index():
    blogs = Blog.query.all()
    return render_template('blog.html',page_title="Build a Blog", 
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
    db.session.add(blog)
    db.session.commit() 
    return redirect('/')

if __name__ == '__main__':
    app.run()