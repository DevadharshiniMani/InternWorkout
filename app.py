#App:(py)
from flask import Flask, render_template, request, redirect, url_for
from models import db, Book

app = Flask(__name__)

# Set up the database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Dev%402002@localhost/book_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the Flask app
db.init_app(app)

@app.route('/')
def home():
    books = Book.query.all()
    return render_template("index.html", books=books)

@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        price = request.form['price']
        new_book = Book(title=title, author=author, genre=genre, price=price)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add_book.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_book(id):
    book = Book.query.get_or_404(id)
    if request.method == 'POST':
        book.title = request.form['title']
        book.author = request.form['author']
        book.genre = request.form['genre']
        book.price = request.form['price']
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit_book.html', book=book)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Creates all the tables defined in models.py
    app.run(debug=True)


#models:(py)
from flask_sqlalchemy import SQLAlchemy

# Initialize the SQLAlchemy object without passing 'app'
db = SQLAlchemy()

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def _repr_(self):
        return f'<Book {self.title}>'
