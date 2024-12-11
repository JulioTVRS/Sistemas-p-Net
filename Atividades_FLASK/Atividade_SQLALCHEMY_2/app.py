
from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import *
from sqlalchemy.orm import *


engine = create_engine('sqlite:///database.db')

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    nome: Mapped[str] = mapped_column(Text, nullable=False)

    def __init__(self, nome):
        self.nome = nome

Base.metadata.create_all(engine)

app = Flask(__name__)

app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        nome = request.form.get('nome')
        session = Session(engine)
        novo_usuario = User(nome=nome)
        session.add(novo_usuario)
        session.commit()
        session.close()

        
        
        return redirect(url_for('register'))
    
    session = Session(engine)
    usuarios = session.query(User).all()
    
    return render_template('register.html', usuarios=usuarios)



