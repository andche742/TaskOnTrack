from sqlalchemy.orm import Session
from db.database import User, get_session

class user_service:
    def create_user(username, password):
        with get_session() as session:
            existing = session.query(User).filter_by(username=username).first()

            if existing:
                raise ValueError("User already exists")
            
            new_user = User(username=username, password=password)

            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            return new_user
    
    def authenticate_user(username, password): # return user if credentials correct
        with get_session() as session:
            user = session.query(User).filter_by(username=username, password=password).first()
            return user
        
    def get_user_by_id(id):
        with get_session() as session:
            user = session.query(User).filter_by(id=id).first()
            return user

    def add_points(user_id, points):
        with get_session() as session:
            user = session.query(User).filter_by(id=user_id).first()
            if user:
                user.points += points
                session.commit()
                session.refresh(user)
            return user
