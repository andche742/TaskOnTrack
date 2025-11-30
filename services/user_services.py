from sqlalchemy.orm import Session
from models.user import User
from db.database import get_session

class UserService:
    def create_user(self, username, password):
        with get_session() as session:
            existing = session.query(User).filter_by(username=username).first()

            if existing:
                raise ValueError("User already exists")
            
            new_user = User(username=username, password=password)

            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            return new_user
    
    def authenticate_user(self, username, password):
        with get_session() as session:
            user = session.query(User).filter_by(username=username, password=password).first()
            return user
        
    def get_user_by_id(self, id):
        with get_session() as session:
            user = session.query(User).filter_by(id=id).first()
            return user
