from model import db, User, Category, DailyTask, CompletedTask, connect_to_db
import datetime

def create_user(email, username, password):
    """Create and return a new user."""

    user = User(email= email, username= username, password= password)

    return user

def get_user_by_email(email):
    return User.query.filter(User.email == email).first()   

def get_daily_task_by_id(task_id):
    return DailyTask.query.get(task_id)

def get_daily_tasks_by_user_id(user_id):
    return DailyTask.query.filter(DailyTask.user_id == int(user_id)).all()

def get_daily_task_by_title(title):
    return DailyTask.query.filter(DailyTask.title == title).first()

def create_daily_task(category_id,user_id,title):
    """Create and return a new user."""

    task = DailyTask(category_id=category_id, user_id=user_id, title=title)

    return task

def get_category_by_title(title):

    return Category.query.filter(Category.title == title).first()


def get_categories(tasks):

    category_set = set()

    for task in tasks:
        category_set.add(task.category_id)

    categories = []

    for cat in category_set:
        category = Category.query.get(cat)
        if category.title == "":
            continue
        else:
            categories.append(category)

    return categories

def create_category(title):

    category = Category(title=title)

    return category

def create_completed_task(qty, notes, date, task_id, category_id, user_id, title):
    """Create and return a new user."""

    task = CompletedTask(qty=qty, 
            notes=notes, 
            date=date, 
            task_id=task_id, 
            category_id=category_id, 
            user_id=user_id, 
            title=title)

    

    return task

def get_completed_tasks_by_user_id(user_id):

    return CompletedTask.query.filter(CompletedTask.user_id == int(user_id)).all()

def filter_completed_tasks_by_category_id(tasks, category_id):

    filtered_tasks = []

    for task in tasks:
        if task.category_id == category_id:
            filtered_tasks.append(task)
    
    return filtered_tasks

def filter_completed_tasks_by_task_id(tasks, task_id):

    filtered_tasks = []

    for task in tasks:
        if task.task_id == task_id:
            filtered_tasks.append(task)
    
    return filtered_tasks

def filter_completed_tasks_by_date(tasks, date_list):

    filtered_tasks = []

    for task in tasks:
        if task.date in date_list:
            filtered_tasks.append(task)
    
    return filtered_tasks

def dictify_task_objects(tasks, days):
    
    task_list = []

    for day in days:
        date = day
        day = {}
        day['qty'] = 0
        day['date'] = date
        task_list.append(day)
        for task in tasks:
            if task.date == date:
                day['qty'] += task.qty
                day['title'] = task.title
    

    return task_list




def get_all_completed():

    return CompletedTask.query.all()

def get_grouped_completed_tasks_by_user(user_id):

    tasks = get_completed_tasks_by_user_id(user_id)

    task_set = set()

    for task in tasks:
        task_set.add(task.task_id)

    task_list = []

    for t in task_set:
        task = CompletedTask.query.get(t)
        task_list.append(task)

    return task_list

def get_days(num_days):

    
    today = datetime.date.today()

    date_list = []

    while num_days >= 0:
        date = today - datetime.timedelta(days=num_days)
        date_list.append(date)
        num_days -= 1

    return date_list