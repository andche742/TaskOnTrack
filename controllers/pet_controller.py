from services.pet_services import pet_service
class pet_controller:
    def get_mood(user_id):
        pet = pet_service.get_pet_by_user(user_id)
        return pet.mood
    
    def get_hunger(user_id):
        pet = pet_service.get_pet_by_user(user_id)
        return pet.hunger
    
    def get_bored(user_id):
        pet = pet_service.get_pet_by_user(user_id)
        return pet.bored