from flask import Flask, render_template, request, jsonify, session
import random
from dotenv import load_dotenv
import os
from matches import get_players_from_url
import hashlib

load_dotenv()

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

def get_seed_from_inputs(team1, team2, form_data):
    """Generate a consistent seed from the input parameters"""
    input_string = f"{team1}-{team2}"
    for key in sorted(form_data.keys()):
        input_string += f"-{key}:{form_data[key]}"
    return int(hashlib.md5(input_string.encode()).hexdigest(), 16)

def get_team_key(team1, team2):
    """Generate a consistent key for team combination"""
    teams = sorted([team1, team2])  # Sort to ensure same key regardless of order
    return f"{teams[0]}-{teams[1]}"

def check_prediction_limit(team1, team2):
    """Check if prediction limit is reached for team combination"""
    team_key = get_team_key(team1, team2)
    predictions = session.get('predictions', {})
    count = predictions.get(team_key, 0)
    return count >= 3

def increment_prediction_count(team1, team2):
    """Increment prediction count for team combination"""
    team_key = get_team_key(team1, team2)
    predictions = session.get('predictions', {})
    predictions[team_key] = predictions.get(team_key, 0) + 1
    session['predictions'] = predictions

def generate_fantasy_11(team1, team2, form_data):
    """Generate fantasy 11 with exactly 6 constant and 5 variable players"""
    # Get all players
    all_players = get_players_from_url(team1, team2)
    
    # Generate base seed from just teams (for constant players)
    core_seed = int(hashlib.md5(f"{team1}-{team2}".encode()).hexdigest(), 16)
    
    # Use a separate random generator for core selection
    core_rng = random.Random(core_seed)
    
    # Select exactly 6 core players
    all_players_copy = all_players.copy()
    core_rng.shuffle(all_players_copy)
    core_players = all_players_copy[:6]
    
    # Get remaining players pool
    remaining_pool = [p for p in all_players if p not in core_players]
    
    # Generate seed for variable players from all form inputs
    variable_seed = get_seed_from_inputs(team1, team2, form_data)
    variable_rng = random.Random(variable_seed)
    
    # Select exactly 5 variable players
    variable_rng.shuffle(remaining_pool)
    variable_players = remaining_pool[:5]
    
    # Combine all players
    final_11 = core_players + variable_players
    
    # Final shuffle with a new seed
    final_seed = variable_seed ^ core_seed  # XOR the seeds
    final_rng = random.Random(final_seed)
    final_rng.shuffle(final_11)
    
    return final_11

@app.route('/')
def home():
    session.clear()
    return render_template('index.html')

@app.route('/get_prediction_count', methods=['POST'])
def get_prediction_count():
    """Get remaining predictions for team combination"""
    team1 = request.form.get('team1')
    team2 = request.form.get('team2')
    
    if team1 and team2:
        team_key = get_team_key(team1, team2)
        predictions = session.get('predictions', {})
        count = predictions.get(team_key, 0)
        return jsonify({
            'remaining': 3 - count,
            'total_used': count
        })
    return jsonify({'error': 'Invalid teams'})

@app.route('/get_popular_picks', methods=['GET'])
def get_popular_picks():
    team1 = request.args.get('team1')
    team2 = request.args.get('team2')

    if not team1 or not team2:
        return jsonify({"error": "Please select both teams first"})

    players_list = get_players_from_url(team1, team2)
    
    seed = int(hashlib.md5(f"{team1}-{team2}".encode()).hexdigest(), 16)
    rng = random.Random(seed)
    shuffled_players = players_list.copy()
    rng.shuffle(shuffled_players)

    return jsonify({"popular_picks": shuffled_players[:5]})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        team1 = request.form.get('team1')
        team2 = request.form.get('team2')

        if team1 == team2:
            return jsonify({'error': 'Please select different teams'})
            
        # Check prediction limit
        if check_prediction_limit(team1, team2):
            return jsonify({'error': 'Prediction limit reached for these teams'})
        
        form_data = request.form.to_dict()
        fantasy_11 = generate_fantasy_11(team1, team2, form_data)
        
        # Increment prediction count
        increment_prediction_count(team1, team2)
        
        # Get remaining predictions
        team_key = get_team_key(team1, team2)
        predictions = session.get('predictions', {})
        remaining = 3 - predictions.get(team_key, 0)
        
        return jsonify({
            'Fantasy 11': fantasy_11,
            'predictions_remaining': remaining
        })
    except Exception as e:
        print(f"Error in predict route: {str(e)}")
        return jsonify({'error': f'An error occurred: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True)