
# main.py

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///news.db'
db = SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    content = db.Column(db.Text)

@app.route('/')
def home():
    articles = Article.query.all()
    return render_template('index.html', articles=articles)

@app.route('/article/<int:id>')
def article(id):
    article = Article.query.get(id)
    return render_template('article.html', article=article)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/admin')
def admin():
    articles = Article.query.all()
    return render_template('admin.html', articles=articles)

@app.route('/add_article', methods=['POST'])
def add_article():
    title = request.form['title']
    content = request.form['content']
    new_article = Article(title=title, content=content)
    db.session.add(new_article)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/edit_article/<int:id>', methods=['POST'])
def edit_article(id):
    article = Article.query.get(id)
    article.title = request.form['title']
    article.content = request.form['content']
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/delete_article/<int:id>')
def delete_article(id):
    article = Article.query.get(id)
    db.session.delete(article)
    db.session.commit()
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run()
