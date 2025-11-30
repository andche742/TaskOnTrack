from ui.app import TaskOnTrackApp 
from db.database import init_db
def main():
    app = TaskOnTrackApp()
    app.mainloop()
    init_db()

if __name__ == "__main__":
    main()