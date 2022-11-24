from ast import For
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from sqlalchemy import create_engine


engine = create_engine(
      "mysql://root:Atas123456-@localhost/ppbd_var2", echo=False)
SessionFactory = sessionmaker(bind=engine)
#session = Session(engine)

Base = declarative_base()


class User(Base):
	__tablename__ = "user"
	id = Column(Integer, primary_key=True, autoincrement=True)
	username = Column(String(45), unique=True)
	first_name = Column(String(45))
	last_name = Column(String(45))
	email = Column(String(45), unique=True)
	password = Column(String(100))
	notes_count = Column(Integer, default=0)


class Notes(Base):
	__tablename__ = "notes"
	id = Column(Integer, primary_key=True)
	title = Column(String(45), nullable=False)
	content = Column(String(404))
	notescol = Column(String(45))
	tags = Column(String(400), nullable=False)
	user_iduser = Column(Integer, ForeignKey("user.id"), nullable=False)


class Access(Base):
	__tablename__ = "access"
	id = Column(Integer, primary_key=True, autoincrement=True)
	user_id = Column(Integer, ForeignKey("user.id"), nullable=False, primary_key=True)
	note_id = Column(Integer, ForeignKey("notes.id"), nullable=False, primary_key=True)
	time = Column(DateTime, nullable=False)


class Change(Base):
	__tablename__ = "change"
	id = Column(Integer, primary_key=True, autoincrement=True)
	user_id = Column(Integer, ForeignKey("user.id"), nullable=False, primary_key=True)
	note_id = Column(Integer, ForeignKey("notes.id"), nullable=False, primary_key=True)
	time = Column(DateTime, nullable=False)


class Tag(Base):
	__tablename__ = "tag"
	id = Column(Integer, primary_key=True, autoincrement=True)
	name = Column(String(45), unique=True)
