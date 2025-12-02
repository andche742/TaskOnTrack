from models.pet import Pet
from db.database import get_session

class pet_service:
    def create_pet(self, user_id, name, type):
        with get_session() as session:
            new_pet = Pet(user_id=user_id, name=name, type=type)

            session.add(new_pet)
            session.commit()
            session.refresh(new_pet)
            return new_pet
        
    def get_pet_by_user(self, user_id):
        with get_session() as session:
            pet = session.query(Pet).filter_by(user_id=user_id).first()
            return pet
        
    def update_pet(self, pet_id, mood=None, hunger=None, bored=None):
        with get_session() as session:
            pet = session.query(Pet).filter_by(id=pet_id).first()
            if pet:
                if mood is not None:
                    pet.mood = mood
                if hunger is not None:
                    pet.hunger = hunger
                if bored is not None:
                    pet.bored = bored
                session.commit()
                session.refresh(pet)
            return pet

