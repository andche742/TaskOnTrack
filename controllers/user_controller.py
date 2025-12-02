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

    def get_points(user_id):
        user = user_service.get_user_by_id(user_id)
        return user.points

    def add_points(user_id, points):
        user = user_service.add_points(user_id, points)
        return user.points
        