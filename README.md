# Timer App

This is a very simple timer app that was made entierly with ChatGPT as a test and at the same time to use the generated app for some data collection.

## Getting started with the application

### Setup
To get started with the virtual environment and installing dependencies:
```bash
# Clone reppo
git clone https://github.com/Lerold/Timer-App.git

# Open folder
cd Timer-App/app

# Create a virtual environment.
python3 -m venv venv

# Activate the virtual environment.
source venv/bin/activate

# Install dependencies.
pip install -r requirements.txt
```

### Initiate database
Initializing the database with the following command:
```bash
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```

### Running the Application
After installing dependencies and initializing the database, run the application with the following command:
```bash
flask run
```
Visit `http://127.0.0.1:5000/` in your browser to see the running app.


## Images of application

### Home View
![Home](/images/Home.png "Home")

### Start New Timer View
![Start New Timer](/images/Start_new_Timer.png "Start New Timer")

### Running Timer View
Adding Entries
![Adding Entries](/images/Adding_entries_1.png "Adding Entries")

Entries Added
![Entries Added](/images/Entries_added.png "Entries Added")

Timer Stopped
![Timer Stopped](/images/Timer_stopped.png "Timer Stopped")

### View previously run timmer
List timers
![List Timers](/images/List_timers.png "List Timers")

Timer Stopped
![View Timer](/images/View_timer.png "View Timer")

### Result of CSV Export
Layout of CSV File
![CSV Layout](/images/csv_file.png "CSV Layout")# Timer_App
