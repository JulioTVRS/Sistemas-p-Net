from sqlalchemy import create_engine, Table, Column, ForeignKey
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column, relationship, List

engine = create_engine('sqlite:///exemplo.db')
session = Session(engine)

class Base(DeclarativeBase):
    pass

estudante_curso = Table(
    "estudantes_cursos",
    Base.metadata,
    Column('estudante_id', ForeignKey('estudantes.id'), primary_key=True),
    Column('curso_id', ForeignKey('cursos.id'), primary_key=True)
)

class Curso(Base):
    __tablename__ = 'cursos'
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str]
    estudantes = relationship('Estudante', back_populates='cursos', secondary=estudante_curso)

class Estudante(Base):
    __tablename__ = 'estudantes'
    id: Mapped[int] = mapped_column(primary_key=True)
    nome:Mapped[str]
    cursos = relationship('Curso', back_populates='estudantes')

    def __repr__(self):
        return f"Estudante({self.id}, {self.nome}, {self.curso_id})"


Base.metadata.create_all(engine)

info = session.query(Curso).get(1)
print(info.estudantes)