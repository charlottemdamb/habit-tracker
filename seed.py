
import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system("dropdb task-tracker")
os.system('createdb task-tracker')
model.connect_to_db(server.app)
model.db.create_all()

category1 = crud.create_category('Health')
model.db.session.add(category1)

for n in range(10):
    email = f"user{n}@test.com"  # Voila! A unique email!
    password = "test"
    username = f'user{n}'

    user = crud.create_user(email, username, password)
    model.db.session.add(user)
    model.db.session.commit()
    category_id = 1
    title = 'Water'

    new_task = crud.create_daily_task(category_id, user.user_id, title)
                                    
    model.db.session.add(new_task)

model.db.session.commit()