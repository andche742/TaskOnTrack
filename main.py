from ui.app import TaskOnTrackApp 
from db.database import init_db
def main():
    init_db()
    app = TaskOnTrackApp()
    app.mainloop()
    

if __name__ == "__main__":
    main()