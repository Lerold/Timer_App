from flask import Flask, render_template, request, redirect, url_for, flash, send_file, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime
import csv
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'some_random_secret_key'  # Change for production

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# ----------------------------------------------------------------------
# MODELS
# ----------------------------------------------------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Add a new column to store who created the timer (foreign key to User)
class Timer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=True)

    # [NEW] The user who created this timer
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    def duration(self):
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return None

    def creator_name(self):
        """Return the username of the user who created this timer."""
        if self.created_by:
            creator = User.query.get(self.created_by)
            return creator.username if creator else "Unknown"
        return "Unknown"

# Add a new column to store who created each entry (foreign key to User)
class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timer_id = db.Column(db.Integer, db.ForeignKey('timer.id'), nullable=False)
    current_date = db.Column(db.String(20), nullable=False)
    current_time = db.Column(db.String(20), nullable=False)
    time_since_start = db.Column(db.String(20), nullable=False)
    tram_line_no = db.Column(db.String(10))
    tram_name = db.Column(db.String(100))
    direction = db.Column(db.String(100))
    rfid_tag = db.Column(db.String(100))
    switch_direction = db.Column(db.String(20))
    free_notes = db.Column(db.Text)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)

    # [NEW] The user who created this entry
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    def creator_name(self):
        """Return the username of the user who created this entry."""
        if self.created_by:
            creator = User.query.get(self.created_by)
            return creator.username if creator else "Unknown"
        return "Unknown"

# ----------------------------------------------------------------------
# DECORATORS
# ----------------------------------------------------------------------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ----------------------------------------------------------------------
# AUTH ROUTES
# ----------------------------------------------------------------------
@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    """
    Only allow user_id=1 to create new users.
    If someone else tries to access, redirect them away.
    """
    if 'user_id' not in session or session['user_id'] != 1:
        flash("Only the user with ID=1 can create new users.")
        return redirect(url_for('login'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username and password:
            existing = User.query.filter_by(username=username).first()
            if existing:
                flash("Username already taken.")
                return redirect(url_for('create_user'))
            new_user = User(username=username)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash("User created! You can now log in.")
            return redirect(url_for('login'))
        else:
            flash("Please enter a username and password.")
    return render_template('create_user.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Removed the 'create_user' link from this template,
    so normal users won't see a direct link to create_user.
    Only user_id=1 can access create_user if they know the URL.
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session['user_id'] = user.id
            flash("Logged in successfully!")
            return redirect(url_for('index'))
        else:
            flash("Invalid username or password.")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for('login'))

# ----------------------------------------------------------------------
# CORE APP ROUTES
# ----------------------------------------------------------------------
@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/start_timer', methods=['GET', 'POST'])
@login_required
def start_timer():
    """
    When a new timer is created, record which user created it (created_by).
    """
    if request.method == 'POST':
        new_timer = Timer(created_by=session['user_id'])
        db.session.add(new_timer)
        db.session.commit()
        return redirect(url_for('edit_timer', timer_id=new_timer.id))
    return render_template('start_timer.html')

@app.route('/edit_timer/<int:timer_id>', methods=['GET', 'POST'])
@login_required
def edit_timer(timer_id):
    timer = Timer.query.get_or_404(timer_id)
    if request.method == 'POST' and not timer.end_time:
        current_date = datetime.now().strftime("%Y-%m-%d")
        current_time = datetime.now().strftime("%H:%M:%S")
        time_since_start_delta = datetime.now() - timer.start_time
        hours, remainder = divmod(time_since_start_delta.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        time_since_start = f"{int(hours)}h {int(minutes)}m {int(seconds)}s"

        tram_line_no = request.form.get("tram_line_no")
        tram_name = request.form.get("tram_name")
        direction = request.form.get("direction")
        rfid_tag = request.form.get("rfid_tag")
        switch_direction = request.form.get("switch_direction")
        free_notes = request.form.get("free_notes")

        lat_str = request.form.get("latitude")
        lon_str = request.form.get("longitude")
        latitude, longitude = None, None
        if lat_str and lon_str:
            try:
                latitude = float(lat_str)
                longitude = float(lon_str)
            except ValueError:
                pass

        # When a user adds an entry, record the user who created it
        new_entry = Entry(
            timer_id=timer.id,
            current_date=current_date,
            current_time=current_time,
            time_since_start=time_since_start,
            tram_line_no=tram_line_no,
            tram_name=tram_name,
            direction=direction,
            rfid_tag=rfid_tag,
            switch_direction=switch_direction,
            free_notes=free_notes,
            latitude=latitude,
            longitude=longitude,
            created_by=session['user_id']
        )
        db.session.add(new_entry)
        db.session.commit()

    entries = Entry.query.filter_by(timer_id=timer.id).all()
    return render_template('new_timer.html', timer=timer, entries=entries)

@app.route('/stop_timer/<int:timer_id>', methods=['POST'])
@login_required
def stop_timer(timer_id):
    timer = Timer.query.get_or_404(timer_id)
    if not timer.end_time:
        timer.end_time = datetime.utcnow()
        db.session.commit()
    return redirect(url_for('view_timer', timer_id=timer.id))

@app.route('/delete_timer/<int:timer_id>', methods=['POST'])
@login_required
def delete_timer(timer_id):
    timer = Timer.query.get_or_404(timer_id)
    # Delete all entries associated with the timer
    Entry.query.filter_by(timer_id=timer.id).delete()
    db.session.delete(timer)
    db.session.commit()
    return redirect(url_for('previous_timers'))

@app.route('/view_timer/<int:timer_id>')
@login_required
def view_timer(timer_id):
    timer = Timer.query.get_or_404(timer_id)
    entries = Entry.query.filter_by(timer_id=timer.id).all()
    if timer.end_time:
        return render_template('view_single_timer.html', timer=timer, entries=entries)
    return render_template('new_timer.html', timer=timer, entries=entries)

@app.route('/export_timer/<int:timer_id>')
@login_required
def export_timer(timer_id):
    """
    Include who created the timer and who created each entry in the CSV.
    """
    timer = Timer.query.get_or_404(timer_id)
    entries = Entry.query.filter_by(timer_id=timer.id).all()
    csv_filename = f"timer_{timer_id}.csv"

    # We'll add two columns: created_by_user (timer), entry_created_by_user (entry)
    with open(csv_filename, 'w', newline='') as csvfile:
        fieldnames = [
            'timer_id',
            'timer_created_by_user',
            'current_date',
            'current_time',
            'time_since_start',
            'tram_line_no',
            'tram_name',
            'direction',
            'rfid_tag',
            'switch_direction',
            'free_notes',
            'entry_created_by_user',
            'latitude',
            'longitude'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # We'll store the timer's creator name once per row, though it's the same for all entries.
        timer_creator = timer.creator_name()

        for entry in entries:
            writer.writerow({
                'timer_id': timer.id,
                'timer_created_by_user': timer_creator,
                'current_date': entry.current_date,
                'current_time': entry.current_time,
                'time_since_start': entry.time_since_start,
                'tram_line_no': entry.tram_line_no,
                'tram_name': entry.tram_name,
                'direction': entry.direction,
                'rfid_tag': entry.rfid_tag,
                'switch_direction': entry.switch_direction,
                'free_notes': entry.free_notes,
                'entry_created_by_user': entry.creator_name(),
                'latitude': entry.latitude if entry.latitude else '',
                'longitude': entry.longitude if entry.longitude else ''
            })
    return send_file(csv_filename, as_attachment=True)

@app.route('/previous_timers')
@login_required
def previous_timers():
    timers = Timer.query.all()
    return render_template('view_timers.html', timers=timers)

if __name__ == '__main__':
    app.run(debug=True)