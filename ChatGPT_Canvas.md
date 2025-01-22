## Project Structure Overview
The app will be built using Flask and have the following structure:
```
project_root/
  ├── app.py
  ├── wsgi.py        (optional if you’re using Gunicorn)
  ├── requirements.txt
  ├── database.sqlite3
  ├── static/
  │    ├── favicon-32x32.png
  │    ├── favicon-16x16.png
  │    ├── apple-touch-icon.png
  │    └── site.webmanifest
  ├── templates/
  │    ├── base.html           <-- [NEW/UPDATED] includes favicon references
  │    ├── index.html
  │    ├── start_timer.html
  │    ├── new_timer.html
  │    ├── view_timers.html
  │    ├── view_single_timer.html
  │    ├── login.html
  │    ├── create_user.html
  └── migrations/              (if using Flask-Migrate)
```

### 1. `requirements.txt`
This file will list all the dependencies.
```
Flask==2.1.0
SQLAlchemy==1.4.39
Flask-SQLAlchemy==2.5.1
Werkzeug==2.1.0
Flask-Migrate==3.1.0
gunicorn==20.1.0
```

### 2. Setting Up a Virtual Environment
To get started with the virtual environment and installing dependencies:
```bash
# Clone or download the project folder.
cd project_root

# Install Python 3.12 venv
sudo apt install python3 python3-venv python3-pip

# Create a virtual environment.
python3 -m venv venv

# Activate the virtual environment.
source venv/bin/activate

# Install dependencies.
pip install -r requirements.txt
```

### 3. Running the Application
After installing dependencies and initializing the database, run the application with the following command:
```bash
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
flask run
```
Visit `http://127.0.0.1:5000/` in your browser to see the running app.

#### Run in Production
```bash
gunicorn wsgi:app --bind 0.0.0.0:5000 --workers 10
```

### Manage users
# Create a user
```bash
python manage_users.py create-user --username alice --password MySecret
```

# List all users
```
python manage_users.py list-users
```

# Rename or reset a user's password
```
python manage_users.py edit-user --old-username alice --new-username alice2 --new-password MyNewPass
```

# Remove a user
```
python manage_users.py remove-user --username alice2
```

### 4. Additional Documentation (`README.md`)
Include the following sections in the README:

- **Project Overview**
- **Setup Instructions**
- **Usage Instructions**
- **Licensing Information**

### 5. License (`LICENSE`)
Include an open source license such as MIT or Apache 


## Images of application

### 