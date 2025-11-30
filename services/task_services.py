from sqlalchemy.orm import Session
from models.task import Task
from db.database import get_session

class TaskService:
    def create_task(self, user_id, title, due_date, description=""):
        with get_session() as session:
            new_task = Task(user_id=user_id, title=title, description=description, due_date=due_date, status="incomplete")

            session.add(new_task)
            session.commit()
            session.refresh(new_task)
            return new_task

    def get_tasks_by_user(self, user_id):
        with get_session() as session:
            tasks = session.query(Task).filter_by(user_id=user_id).all()
            return tasks
        
    def delete_task(self, task_id):
        with get_session() as session:
            task = session.query(Task).filter_by(id=task_id).first()
            if task:
                session.delete(task)
                session.commit()
            return task
        
    def get_task_by_id(self, task_id):
        with get_session() as session:
            task = session.query(Task).filter_by(id=task_id).first()
            return task
    
    def update_task(self, task_id, title=None, description=None, due_date=None, status=None):
        with get_session() as session:
            task = session.query(Task).filter_by(id=task_id).first()
            if task:
                if title is not None:
                    task.title = title
                if description is not None:
                    task.description = description
                if due_date is not None:
                    task.due_date = due_date
                if status is not None:
                    task.status = status
                session.commit()
                session.refresh(task)
            return task
        
    