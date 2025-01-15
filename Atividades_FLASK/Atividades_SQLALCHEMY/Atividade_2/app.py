from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(nullable=False)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projeto.db'

db.init_app(app)


with app.app_context():
    db.create_all()

@app.route('/')
def index():
    user = User(nome="Pessoa")

    db.session.add(user)
    db.session.commit()
    db.session.close()

    return render_template('index.html')

@app.route('/listar')
def listar():
    resultado = db.session.query(User).all()
    return render_template('listar.html', resultado=resultado)