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
        self.body = body


@app.route('/', methods=['POST', 'GET'])
def index():
    blogs = Blog.query.all()
    return render_template('blog.html',title="Build a Blog", 
        blogs=blogs)


@app.route('/newpost', methods=['POST'])
def new_post():

    blog_id = int(request.form['blog-id'])
    blog = Blog.query.get(blog_id)
    db.session.add(blog)
    db.session.commit()

    return redirect('/')


if __name__ == '__main__':
    app.run()