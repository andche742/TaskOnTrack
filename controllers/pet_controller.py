from services.pet_services import pet_service
class pet_controller:
    def get_mood(user_id):
        pet = pet_service.get_pet_by_user(user_id)
        if not pet:
            return "normal"
        return pet.mood
    
    def get_hunger(user_id):
        pet = pet_service.get_pet_by_user(user_id)
        if not pet:
            return 100
        return pet.hunger
    
    def get_bored(user_id):
        pet = pet_service.get_pet_by_user(user_id)
        if not pet:
            return 100
        return pet.bored
    
    def update_pet_over_time(user_id):
        try:
            pet = pet_service.decay_and_update_mood(user_id)
            if not pet:
                return False, "Pet not found"
            return True, pet
        except Exception as e:
            return False, str(e)
    
    def update_pet_stats(user_id, hunger_change=None, boredom_change=None):
        try:
            pet = pet_service.get_pet_by_user(user_id)
            if not pet:
                return False, "Pet not found"
            
            new_hunger = pet.hunger
            new_bored = pet.bored
            
            if hunger_change is not None:
                new_hunger = max(0, min(100, pet.hunger + hunger_change))
            
            if boredom_change is not None:
                new_bored = max(0, min(100, pet.bored + boredom_change))
            
            updated_pet = pet_service.update_pet(
                pet.id,
                hunger=new_hunger,
                bored=new_bored
            )
            
            new_mood = pet_service._calculate_mood_from_stats(new_hunger, new_bored)
            updated_pet = pet_service.update_pet(pet.id, mood=new_mood)
            
            return True, updated_pet
        except Exception as e:
            return False, str(e)