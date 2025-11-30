from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base

db_file = "sqlite:///taskontrack.db"

engine = create_engine(db_file)
Session = sessionmaker(bind=engine)
Base = declarative_base()

def get_session():
    return Session()

def init_db():
    Base.metadata.create_all(engine)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    points = Column(Integer, default=0, nullable=False) # points earned by completing tasks, spend on pet care (feed play pat etc)

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String) # optional
    due_date = Column(String, nullable=False)
    status = Column(String, default='incomplete', nullable=False) # incomplete, complete

class Pet(Base):
    __tablename__ = 'pets'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    mood = Column(String, default='happy', nullable=False)  # happy hungry bored etc
    hunger = Column(Integer, default=100, nullable=False)  # use this to incentivize user to feed
    bored = Column(Integer, default=100, nullable=False)  # use this to incentivize user to play