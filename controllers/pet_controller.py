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