from sqlalchemy import Integer, String, Text, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, Mapped, mapped_column, relationship
from flask_login import UserMixin
from datetime import datetime, timezone

engine = create_engine('sqlite:///database.db')

class Base(DeclarativeBase):
    pass

class User(Base, UserMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(Text, nullable=False)
    books: Mapped[list['Book']] = relationship("Book", backref='owner')

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    genre: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    def __init__(self, title, genre, user_id):
        self.title = title
        self.genre = genre
        self.user_id = user_id

Base.metadata.create_all(engine)

session = Session(bind=engine)