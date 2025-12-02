from services.pet_services import pet_service
class pet_controller:
    def get_mood(user_id):
        pet = pet_service.get_pet_by_user(user_id)
        return pet.mood