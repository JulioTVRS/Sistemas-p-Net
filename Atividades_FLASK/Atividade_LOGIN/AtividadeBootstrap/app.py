from flask import Flask, render_template, url_for, redirect, request
from werkzeug.security import generate_password_hash, check_password_hash
from models import *
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

app = Flask(__name__)

app.config['SECRET_KEY'] = "SUPERSECRETO"

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(user_id)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        existing_user = session.query(User).filter_by(email=email).first()

        if existing_user:
            return "<h1>E-mail já registrado em outra conta.</h1>"

        hashed_password = generate_password_hash(password)

        user = User(name=name, email=email, password=hashed_password)
        session.add(user)
        session.commit()
        login_user(user)

        return redirect(url_for('dash'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        
        user = session.query(User).filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)

            return redirect(url_for('dash'))

    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dash():
    users = session.query(User).all()
    books = session.query(Book).filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', users=users, books=books)

@app.route('/edituser/<int:id>', methods=['GET','POST'])
@login_required
def edit_user(id):
    user = session.query(User).get(id)
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']

        user.name = name
        user.email = email

        session.commit()

        return redirect(url_for('dash'))

    return render_template('edit_user.html', user=user)

@app.route('/deleteuser/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_user(id):
    user = session.query(User).get(id)
    if request.method == "POST":
        session.delete(user)
        session.commit()

        return redirect(url_for('dash'))
    
@app.route('/create_book', methods=['GET', 'POST'])
@login_required
def create_book():
    if request.method == 'POST':
        title = request.form['title']
        genre = request.form['genre']

        book = Book(title=title, genre=genre, user_id=current_user.id)
        session.add(book)
        session.commit()

        return redirect(url_for('dash'))

    return render_template('create_book.html') 


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))