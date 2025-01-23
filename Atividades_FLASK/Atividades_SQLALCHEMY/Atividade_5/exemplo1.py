from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, DeclarativeBase, mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey
from typing import List

engine = create_engine('sqlite:///exemplo1.db')
session = Session(bind=engine)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str]
    gerente_id = mapped_column(ForeignKey('users.id'), nullable=True)


    gerenciados: Mapped[List['User']] = relationship('User', back_populates='gerente')

    gerente = relationship('User', back_populates='gerenciados', remote_side=[id])

    def __repr__(self):
        return self.nome

Base.metadata.create_all(bind=engine)

# user1 = User(nome='Hugo')
# session.add(user1)
# session.commit()

# user2 = User(nome='João', gerente_id=1)
# user3 = User(nome='Maria', gerente_id=1)
# user4 = User(nome='Pedro')

# session.add_all([user2, user3, user4])
# session.commit()

sttm = select(User).where(User.gerente_id == 1)