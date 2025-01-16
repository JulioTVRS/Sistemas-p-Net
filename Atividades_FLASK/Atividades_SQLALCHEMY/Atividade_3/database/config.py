import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Configuração do banco de dados
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'projeto.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
