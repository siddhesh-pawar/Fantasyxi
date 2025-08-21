import os
import logging
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import random
from dotenv import load_dotenv
import hashlib
import re

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO if os.environ.get('FLASK_ENV') == 'production' else logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)



# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
if not app.config['SECRET_KEY']:
    raise ValueError("No SECRET_KEY set for Flask application")

# Database configuration
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///fantasy11.db')
# Handle Render's postgres:// URL (needs to be postgresql://)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 10,
    'pool_recycle': 3600,
    'pool_pre_ping': True
}

# Security configurations
app.config['SESSION_COOKIE_SECURE'] = os.environ.get('FLASK_ENV') == 'production'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
app.config['WTF_CSRF_ENABLED'] = True
app.config['WTF_CSRF_TIME_LIMIT'] = None

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

# User Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    favorite_team = db.Column(db.String(100))
    predictions_count = db.Column(db.Integer, default=0)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

# Prediction History Model
class PredictionHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    team1 = db.Column(db.String(100), nullable=False)
    team2 = db.Column(db.String(100), nullable=False)
    predicted_team = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    user = db.relationship('User', backref=db.backref('predictions', lazy=True))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Utility functions
def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    return True, "Password is valid"

def get_seed_from_inputs(team1, team2, form_data):
    """Generate a consistent seed from the input parameters"""
    input_string = f"{team1}-{team2}"
    for key in sorted(form_data.keys()):
        if key not in ['csrf_token', 'team1', 'team2']:  # Exclude CSRF token and team names
            input_string += f"-{key}:{form_data[key]}"
    return int(hashlib.md5(input_string.encode()).hexdigest(), 16)

def get_players_pool(team1, team2):
    """Get players for the given teams - Replace with your actual implementation"""
    # This is a placeholder - implement your actual player fetching logic here
    # You might want to use an API or database to get real player data
    
    team_players = {
        "Chennai Super Kings": ["MS Dhoni", "Ruturaj Gaikwad", "Devon Conway", "Ravindra Jadeja", 
                               "Moeen Ali", "Deepak Chahar", "Tushar Deshpande", "Matheesha Pathirana"],
        "Mumbai Indians": ["Rohit Sharma", "Ishan Kishan", "Suryakumar Yadav", "Tilak Varma", 
                          "Hardik Pandya", "Tim David", "Jasprit Bumrah", "Piyush Chawla"],
        "Royal Challengers Bengaluru": ["Virat Kohli", "Faf du Plessis", "Glenn Maxwell", "Cameron Green",
                                        "Dinesh Karthik", "Mohammed Siraj", "Josh Hazlewood", "Wanindu Hasaranga"],
        "Kolkata Knight Riders": ["Shreyas Iyer", "Nitish Rana", "Rinku Singh", "Andre Russell",
                                  "Sunil Narine", "Venkatesh Iyer", "Varun Chakravarthy", "Mitchell Starc"],
        "Delhi Capitals": ["David Warner", "Prithvi Shaw", "Mitchell Marsh", "Rishabh Pant",
                          "Axar Patel", "Kuldeep Yadav", "Anrich Nortje", "Ishant Sharma"],
        "Rajasthan Royals": ["Yashasvi Jaiswal", "Jos Buttler", "Sanju Samson", "Shimron Hetmyer",
                            "Ravichandran Ashwin", "Yuzvendra Chahal", "Trent Boult", "Prasidh Krishna"],
        "Punjab Kings": ["Shikhar Dhawan", "Jonny Bairstow", "Liam Livingstone", "Jitesh Sharma",
                        "Sam Curran", "Arshdeep Singh", "Kagiso Rabada", "Rahul Chahar"],
        "Sunrisers Hyderabad": ["Abhishek Sharma", "Travis Head", "Aiden Markram", "Heinrich Klaasen",
                               "Abdul Samad", "Pat Cummins", "Bhuvneshwar Kumar", "T Natarajan"],
        "Gujarat Titans": ["Shubman Gill", "Wriddhiman Saha", "Hardik Pandya", "David Miller",
                          "Rahul Tewatia", "Rashid Khan", "Mohammed Shami", "Josh Little"],
        "Lucknow Super Giants": ["KL Rahul", "Quinton de Kock", "Marcus Stoinis", "Nicholas Pooran",
                                 "Krunal Pandya", "Ravi Bishnoi", "Mark Wood", "Avesh Khan"]
    }
    
    players1 = team_players.get(team1, [f"{team1} Player {i}" for i in range(1, 9)])
    players2 = team_players.get(team2, [f"{team2} Player {i}" for i in range(1, 9)])
    
    return players1 + players2

def generate_fantasy_11(team1, team2, form_data):
    """Generate fantasy 11 with exactly 6 constant and 5 variable players"""
    try:
        all_players = get_players_pool(team1, team2)
        
        if len(all_players) < 11:
            logger.warning(f"Not enough players for {team1} vs {team2}")
            return all_players  # Return what we have
        
        # Core players (constant for team combination)
        core_seed = int(hashlib.md5(f"{team1}-{team2}".encode()).hexdigest(), 16)
        core_rng = random.Random(core_seed)
        
        all_players_copy = all_players.copy()
        core_rng.shuffle(all_players_copy)
        core_players = all_players_copy[:6]
        
        # Variable players based on user preferences
        remaining_pool = [p for p in all_players if p not in core_players]
        
        variable_seed = get_seed_from_inputs(team1, team2, form_data)
        variable_rng = random.Random(variable_seed)
        
        variable_rng.shuffle(remaining_pool)
        variable_players = remaining_pool[:5]
        
        # Final team
        final_11 = core_players + variable_players
        
        final_seed = variable_seed ^ core_seed
        final_rng = random.Random(final_seed)
        final_rng.shuffle(final_11)
        
        return final_11
    except Exception as e:
        logger.error(f"Error generating fantasy 11: {str(e)}")
        return []

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    logger.error(f"Internal error: {str(error)}")
    return render_template('500.html'), 500

# Authentication Routes
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        errors = []
        
        if not username or len(username) < 3:
            errors.append('Username must be at least 3 characters long')
        
        if not email or not validate_email(email):
            errors.append('Please enter a valid email address')
        
        if password != confirm_password:
            errors.append('Passwords do not match')
        
        is_valid, password_msg = validate_password(password)
        if not is_valid:
            errors.append(password_msg)
        
        if User.query.filter_by(username=username).first():
            errors.append('Username already exists')
        
        if User.query.filter_by(email=email).first():
            errors.append('Email already registered')
        
        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('register.html')
        
        user = User(username=username, email=email)
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            logger.info(f"New user registered: {username}")
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            logger.error(f"Registration error: {str(e)}")
            flash('An error occurred during registration. Please try again.', 'danger')
            return render_template('register.html')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        username_or_email = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        remember = request.form.get('remember', False)
        
        user = User.query.filter(
            (User.username == username_or_email) | 
            (User.email == username_or_email.lower())
        ).first()
        
        if user and user.check_password(password):
            if not user.is_active:
                flash('Your account has been deactivated. Please contact support.', 'warning')
                return render_template('login.html')
            
            login_user(user, remember=remember)
            logger.info(f"User logged in: {user.username}")
            
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username/email or password', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    username = current_user.username
    logout_user()
    logger.info(f"User logged out: {username}")
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('login'))

@app.route('/profile')
@login_required
def profile():
    predictions = PredictionHistory.query.filter_by(user_id=current_user.id)\
                                         .order_by(PredictionHistory.created_at.desc())\
                                         .limit(10).all()
    return render_template('profile.html', user=current_user, predictions=predictions)

@app.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    email = request.form.get('email', '').strip().lower()
    favorite_team = request.form.get('favorite_team', '').strip()
    
    if email and validate_email(email):
        existing_user = User.query.filter_by(email=email).first()
        if existing_user and existing_user.id != current_user.id:
            flash('Email already in use by another account.', 'danger')
        else:
            current_user.email = email
    
    if favorite_team:
        current_user.favorite_team = favorite_team
    
    try:
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        logger.info(f"Profile updated for user: {current_user.username}")
    except Exception as e:
        db.session.rollback()
        logger.error(f"Profile update error: {str(e)}")
        flash('An error occurred while updating profile.', 'danger')
    
    return redirect(url_for('profile'))

@app.route('/change_password', methods=['POST'])
@login_required
def change_password():
    current_password = request.form.get('current_password', '')
    new_password = request.form.get('new_password', '')
    confirm_password = request.form.get('confirm_new_password', '')
    
    if not current_user.check_password(current_password):
        flash('Current password is incorrect.', 'danger')
        return redirect(url_for('profile'))
    
    if new_password != confirm_password:
        flash('New passwords do not match.', 'danger')
        return redirect(url_for('profile'))
    
    is_valid, password_msg = validate_password(new_password)
    if not is_valid:
        flash(password_msg, 'danger')
        return redirect(url_for('profile'))
    
    current_user.set_password(new_password)
    
    try:
        db.session.commit()
        flash('Password changed successfully!', 'success')
        logger.info(f"Password changed for user: {current_user.username}")
    except Exception as e:
        db.session.rollback()
        logger.error(f"Password change error: {str(e)}")
        flash('An error occurred while changing password.', 'danger')
    
    return redirect(url_for('profile'))

# Main Routes
@app.route('/')
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/get_popular_picks', methods=['GET'])
@login_required
def get_popular_picks():
    team1 = request.args.get('team1')
    team2 = request.args.get('team2')

    if not team1 or not team2:
        return jsonify({"error": "Please select both teams first"}), 400

    try:
        players_list = get_players_pool(team1, team2)
        
        seed = int(hashlib.md5(f"{team1}-{team2}".encode()).hexdigest(), 16)
        rng = random.Random(seed)
        shuffled_players = players_list.copy()
        rng.shuffle(shuffled_players)

        return jsonify({"popular_picks": shuffled_players[:5]})
    except Exception as e:
        logger.error(f"Error getting popular picks: {str(e)}")
        return jsonify({"error": "Error fetching popular picks"}), 500

@app.route('/predict', methods=['POST'])
@login_required
def predict():
    try:
        team1 = request.form.get('team1')
        team2 = request.form.get('team2')

        if not team1 or not team2:
            return jsonify({'error': 'Please select both teams'}), 400

        if team1 == team2:
            return jsonify({'error': 'Please select different teams'}), 400
        
        form_data = request.form.to_dict()
        fantasy_11 = generate_fantasy_11(team1, team2, form_data)
        
        if not fantasy_11:
            return jsonify({'error': 'Unable to generate team. Please try again.'}), 500
        
        # Save prediction to history
        prediction_history = PredictionHistory(
            user_id=current_user.id,
            team1=team1,
            team2=team2,
            predicted_team=str(fantasy_11)
        )
        
        current_user.predictions_count = (current_user.predictions_count or 0) + 1
        
        db.session.add(prediction_history)
        db.session.commit()
        
        logger.info(f"Prediction generated for user {current_user.username}: {team1} vs {team2}")
        
        return jsonify({'Fantasy 11': fantasy_11})
    except Exception as e:
        logger.error(f"Error in predict route: {str(e)}")
        db.session.rollback()
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/health')
def health():
    """Health check endpoint for monitoring"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()})

# Create tables if they don't exist (for initial deployment)
with app.app_context():
    try:
        db.create_all()
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {str(e)}")

if __name__ == '__main__':
    # Never run with debug=True in production
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))