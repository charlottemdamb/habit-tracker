"""table models for daily tracker project"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    """A user."""

    __tablename__ =  'users'

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    email = db.Column(db.String, unique=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    tasks = db.relationship("DailyTask", back_populates="user")
    comp_tasks = db.relationship("CompletedTask", back_populates="user")

    def __repr__(self):
        return f'<User user_id={self.user_id} username={self.username}>'
    
class Category(db.Model):

    __tablename__ =  'categories'

    category_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String)

    tasks = db.relationship("DailyTask", back_populates="category")
    comp_tasks = db.relationship("CompletedTask", back_populates="category")


    def __repr__(self):
        return f"<Category category_id={self.category_id} title={self.title}>"

class DailyTask(db.Model):
    __tablename__ = "daily-tasks"
    
    
    task_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.category_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))


    category = db.relationship("Category", back_populates="tasks")
    user = db.relationship("User", back_populates="tasks")

    def __repr__(self):
        return f"<DailyTask: task_id={self.task_id} title={self.title}>"

class CompletedTask(db.Model):

    __tablename__ = "completed-tasks"
    
    
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String)
    notes = db.Column(db.Text)
    qty = db.Column(db.Integer)
    date = db.Column(db.Date)
    task_id = db.Column(db.Integer, db.ForeignKey("daily-tasks.task_id"))
    category_id = db.Column(db.Integer, db.ForeignKey("categories.category_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))


    category = db.relationship("Category", back_populates="comp_tasks")
    user = db.relationship("User", back_populates="comp_tasks")
    
    def __repr__(self):
        return f"<CompletedTask: id={self.id} title={self.title}>"


def connect_to_db(flask_app, db_uri="postgresql:///task-tracker", echo=False):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)
    db.create_all()

    print("Connected to the db!")

if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)