"""Server for daily tracker app."""
from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify)
from model import connect_to_db, db
import crud
import datetime
from jinja2 import StrictUndefined


app = Flask(__name__)
app.secret_key = "yoyoma"
app.jinja_env.undefined = StrictUndefined

@app.route ("/")        
def homepage():
    """Homepage.html"""
    user_email = session.get('email', None)
    user = crud.get_user_by_email(user_email)

    if user == None:
        return render_template("homepage.html")
    else:
        return redirect(f"/profile/{user.user_id}")


@app.route("/users", methods= ["POST"])
def register_users():
    """View all users."""
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    curr_user = crud.get_user_by_email(email)
    
    if curr_user:
       flash('Try again with a new email.')
       
    else:
       user = crud.create_user(email, username, password)
       db.session.add(user)
       db.session.commit()
       flash('Your account was created successfully! You can now log in.')

    return redirect("/")

@app.route("/login", methods= ["POST"])
def login_user():

    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)

    if user and password == user.password: 
       
        session['email'] = user.email

        return redirect(f"/profile/{user.user_id}")

    else:

        flash('Incorrect email or password')
        return redirect('/')

@app.route("/logout-page")
def log_out_page():

    return render_template('logout.html')

@app.route("/logout", methods=["POST"])
def logout():
    session.pop('email', None)
    return redirect("/")

@app.route("/profile/<user_id>")
def user_page(user_id):
    user_email = session['email']
    user = crud.get_user_by_email(user_email)
    tasks = crud.get_daily_tasks_by_user_id(user.user_id)
   

    return render_template('profile.html', user=user, tasks=tasks)

@app.route("/save-task", methods= ["POST"])
def save_completeted_tasks():
    
    completed_ids = request.form.getlist("completed")
   
    
    for id in completed_ids:
        qty = int(request.form.get(f"qty-{id}"))
        notes = request.form.get(f"task-notes-{id}")
        today = datetime.date.today()
        task = crud.get_daily_task_by_id(id)
        task_id = id
        category_id = task.category_id
        user_id = task.user_id
        title = task.title
        comp_task = crud.create_completed_task(qty, notes, today, task_id, category_id, user_id, title)
        db.session.add(comp_task)
        db.session.commit()

    flash('Tasks saved!')
    return redirect("/profile/<user_id>")

@app.route("/completed-tasks")
def create_task_page():
    user = crud.get_user_by_email(session['email'])
    tasks = crud.get_daily_tasks_by_user_id(user.user_id)
    comptasks = crud.get_completed_tasks_by_user_id(user.user_id)

    return render_template('completed-task.html', tasks=tasks, comptasks=comptasks)

@app.route('/task-data', methods= ["POST"])
def task_charts():
    user = crud.get_user_by_email(session['email'])
    task = int(request.json.get('task'))
    
    last_week = crud.get_days(7)
    last_month = crud.get_days(30)
    last_year = crud.get_days(365)
    task_list = crud.get_completed_tasks_by_user_id(user.user_id)
    task_by_id = crud.filter_completed_tasks_by_task_id(task_list, task)
    week_tasks = crud.filter_completed_tasks_by_date(task_by_id, last_week)
    month_tasks = crud.filter_completed_tasks_by_date(task_by_id, last_month)
    year_tasks = crud.filter_completed_tasks_by_date(task_by_id, last_year)
    daily_tasks = crud.get_daily_tasks_by_user_id(user.user_id)
   
    all_tasks_list = []
    for task in daily_tasks:
        tasks = crud.filter_completed_tasks_by_task_id(task_list, task.task_id)
        all_month_tasks = crud.filter_completed_tasks_by_date(tasks, last_month)
        all_monthly_task_dicts = crud.dictify_task_objects(all_month_tasks, last_month)
        all_tasks_list.append(all_monthly_task_dicts)
        print(all_tasks_list)
    
    weekly_task_dicts = crud.dictify_task_objects(week_tasks, last_week)
    monthly_task_dicts = crud.dictify_task_objects(month_tasks, last_month)
    yearly_task_dicts = crud.dictify_task_objects(year_tasks, last_year)

    return jsonify ({'week': weekly_task_dicts, 'month': monthly_task_dicts, 'year': yearly_task_dicts, 'all': all_tasks_list})


@app.route("/new-task", methods= ["POST"])
def create_task():
    
    user = crud.get_user_by_email(session['email'])
    category = request.form.get('category', None)
    title = request.form.get('title')


    if category == None:

        user_id = user.user_id
        category_id = None
        new_task = crud.create_daily_task(category_id,user_id,title)
        db.session.add(new_task)
        db.session.commit()

    else:

        cat = crud.get_category_by_title(category)

        if cat == None:

            cat = crud.create_category(category)
            db.session.add(cat)
            db.session.commit()
  
        category_id = cat.category_id
        user_id = user.user_id
        new_task = crud.create_daily_task(category_id,user_id,title)
        db.session.add(new_task)
        db.session.commit()
        flash('New task added!')
    
       
    

    return redirect(f'/profile/{user_id}')


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", port=5000, debug=True)
