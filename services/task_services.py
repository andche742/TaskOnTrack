from sqlalchemy.orm import Session
from db.database import Task,get_session

class task_service:
    def create_task(user_id, title, due_date, description=""):
        with get_session() as session:
            new_task = Task(user_id=user_id, title=title, description=description, due_date=due_date, status="incomplete") # default task to incomplete

            session.add(new_task)
            session.commit()
            session.refresh(new_task)
            return new_task

    def get_tasks_by_user(user_id): # to display all tasks
        with get_session() as session:
            tasks = session.query(Task).filter_by(user_id=user_id).all()
            return tasks
    
    def get_tasks_for_today(user_id): # to display today's tasks
        from datetime import datetime
        today_date = datetime.now().strftime("%m-%d-%Y")
        with get_session() as session:
            tasks = session.query(Task).filter_by(user_id=user_id, due_date=today_date).all()
            return tasks
        
    def delete_task(task_id):
        with get_session() as session:
            task = session.query(Task).filter_by(id=task_id).first()
            if task:
                session.delete(task)
                session.commit()
            return task
        
    def get_task_by_id(task_id):
        with get_session() as session:
            task = session.query(Task).filter_by(id=task_id).first()
            return task
    
    def update_task(task_id, title=None, description=None, due_date=None, status=None): # for editing tasks
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
        
    