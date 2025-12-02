from services.task_services import task_service
from services.user_services import user_service
    
class task_controller:
    def create_task(user_id, title, due_date, description=""):
        try:         
            task = task_service.create_task(user_id, title, due_date, description)
            return True, task
        except Exception as e:
            return False, "Failed to create task"
    
    def get_tasks_by_user(user_id):
        try:
            tasks = task_service.get_tasks_by_user(user_id)
            return True, tasks if tasks else []
        except Exception as e:
            return False, "Failed to load tasks"
    
    def get_tasks_for_today(user_id):
        try:
            tasks = task_service.get_tasks_for_today(user_id)
            return True, tasks if tasks else []
        except Exception as e:
            return False, f"Failed to load tasks for today: {str(e)}"
    
    def delete_task(task_id):
        try:
            task = task_service.delete_task(task_id)
            if not task:
                return False, "Task not found"
            return True, task
        except Exception as e:
            return False, "Failed to delete task"
    
    def edit_task(task_id, title=None, description=None, due_date=None, status=None):
        try:
            task = task_service.update_task(task_id, title, description, due_date, status)
            if not task:
                return False, "Task not found"
            return True, task
        except Exception as e:
            return False, "Failed to update task"
    
    def get_task_by_id(task_id):
        try:
            task = task_service.get_task_by_id(task_id)
            if not task:
                return False, "Task not found"
            return True, task
        except Exception as e:
            return False, "Failed to load task"