from services.user_services import user_service
class user_controller:
    def login(username, password):
        user = user_service.authenticate_user(username, password)
        if not user:
            return False, "Invalid username or password"
        return True, user
    
    def create_account(username, password):
        try:
            user = user_service.create_user(username, password)
            return True, user
        except ValueError:
            return False, "Username already exists"

    