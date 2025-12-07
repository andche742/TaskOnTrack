from db.database import get_session, Pet
from datetime import datetime

class pet_service:
    def create_pet(user_id, name):
        with get_session() as session:
            new_pet = Pet(user_id=user_id, name=name, last_updated=datetime.now()) # init pet with curr time

            session.add(new_pet)
            session.commit()
            session.refresh(new_pet)
            return new_pet
        
    def get_pet_by_user(user_id):
        with get_session() as session:
            pet = session.query(Pet).filter_by(user_id=user_id).first()
            return pet
        
    def update_pet(pet_id, mood=None, hunger=None, bored=None):
        with get_session() as session:
            pet = session.query(Pet).filter_by(id=pet_id).first()
            if pet:
                if mood is not None:
                    pet.mood = mood
                if hunger is not None:
                    pet.hunger = max(0, min(100, hunger)) # clamp between 0 and 100
                if bored is not None:
                    pet.bored = max(0, min(100, bored)) # clamp between 0 and 100
                session.commit()
                session.refresh(pet)
            return pet
    
    def decay_and_update_mood(user_id):
        
        with get_session() as session:
            pet = session.query(Pet).filter_by(user_id=user_id).first()
            if not pet:
                # create pet if user has none
                print(f"Creating default pet for user_id {user_id}")
                pet = Pet(user_id=user_id, mood="normal", hunger=100, bored=100, last_updated=datetime.now())
                session.add(pet)
                session.commit()
                session.refresh(pet)
                return pet
            
            now = datetime.now()
            
            last_update = pet.last_updated
            if last_update is None:
                last_update = now
            
            time_elapsed = (now - last_update).total_seconds()/3600 # in hours
            
            hunger_decay_per_hour = 4  # decay 4 points per hour (96 points per day)
            boredom_decay_per_hour = 4  # decay 4 points per hour (96 points per day)
            
            hunger_decay = hunger_decay_per_hour * time_elapsed
            boredom_decay = boredom_decay_per_hour * time_elapsed
            
            old_hunger = pet.hunger
            old_bored = pet.bored
            
            new_hunger = max(0, pet.hunger - hunger_decay)
            new_bored = max(0, pet.bored - boredom_decay)
            
            pet.hunger = int(new_hunger)
            pet.bored = int(new_bored)
            
            new_mood = pet_service._calculate_mood_from_stats(new_hunger, new_bored)
            pet.mood = new_mood
            
            pet.last_updated = now
            
            session.commit()
            session.refresh(pet)
            print(f"Pet update: user_id={user_id}, time_elapsed={time_elapsed:.2f}s")
            print(f"  Hunger: {old_hunger} -> {pet.hunger} (decay: {hunger_decay:.2f})")
            print(f"  Bored: {old_bored} -> {pet.bored} (decay: {boredom_decay:.2f})")
            print(f"  Mood: {pet.mood}")
            return pet
    
    def _calculate_mood_from_stats(hunger, bored):
        hunger_threshold = 30 
        boredom_threshold = 30 
        
        if hunger <= hunger_threshold and bored <= boredom_threshold:
            return "sad"
        elif hunger <= hunger_threshold:
            return "hungry"
        elif bored <= boredom_threshold:
            return "bored"
        else:
            return "normal" 
    

