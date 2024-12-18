from flask import Flask, render_template
from users import users
from users.models import User
from books import books
from auth import bp
from auth.bp import login_manager
from flask_login import LoginManager

# importar auth_bluprint e login_manager (PROVA)

app = Flask(__name__, template_folder='templates')

app.config['SECRET_KEY'] = 'SUPERSECRETO'

login_manager.init_app(app)
login_manager.login_view = 'auth.login'

app.register_blueprint(users.bp)
app.register_blueprint(books.bp)
app.register_blueprint(bp.bp)

@app.route('/')
def index():
    return render_template('layout.html')