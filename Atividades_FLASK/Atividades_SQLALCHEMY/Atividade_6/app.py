from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///locadora.db'
db = SQLAlchemy(app)

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)

class Veiculo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    modelo = db.Column(db.String(100), nullable=False)
    placa = db.Column(db.String(20), unique=True, nullable=False)

class Locacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    veiculo_id = db.Column(db.Integer, db.ForeignKey('veiculo.id'), nullable=False)
    cliente = db.relationship('Cliente', backref='locacoes')
    veiculo = db.relationship('Veiculo', backref='locacoes')

with app.app_context():
        db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/clientes')
def listar_clientes():
    clientes = Cliente.query.all()
    return render_template('clientes.html', clientes=clientes)

@app.route('/veiculos')
def listar_veiculos():
    veiculos = Veiculo.query.all()
    return render_template('veiculos.html', veiculos=veiculos)

@app.route('/locacoes')
def listar_locacoes():
    locacoes = Locacao.query.all()
    return render_template('locacoes.html', locacoes=locacoes)

@app.route('/cadastrar_cliente', methods=['GET', 'POST'])
def cadastrar_cliente():
    if request.method == 'POST':
        nome = request.form.get('nome')
        telefone = request.form.get('telefone')
        if nome and telefone:
            cliente = Cliente(nome=nome, telefone=telefone)
            db.session.add(cliente)
            db.session.commit()
            return redirect(url_for('listar_clientes'))
    return render_template('cadastrar_cliente.html')

@app.route('/cadastrar_veiculo', methods=['GET', 'POST'])
def cadastrar_veiculo():
    if request.method == 'POST':
        modelo = request.form.get('modelo')
        placa = request.form.get('placa')
        if modelo and placa:
            veiculo = Veiculo(modelo=modelo, placa=placa)
            db.session.add(veiculo)
            db.session.commit()
            return redirect(url_for('listar_veiculos'))
    return render_template('cadastrar_veiculo.html')

@app.route('/cadastrar_locacao', methods=['GET', 'POST'])
def cadastrar_locacao():
    clientes = Cliente.query.all()
    veiculos = Veiculo.query.all()
    
    if request.method == 'POST':
        cliente_id = request.form.get('cliente_id')
        veiculo_id = request.form.get('veiculo_id')
        if cliente_id and veiculo_id:
            locacao = Locacao(cliente_id=cliente_id, veiculo_id=veiculo_id)
            db.session.add(locacao)
            db.session.commit()
            return redirect(url_for('listar_locacoes'))
    
    return render_template('cadastrar_locacao.html', clientes=clientes, veiculos=veiculos)

