from flask import Flask, render_template, request, jsonify, session
import random
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from matches import get_players_from_url
import hashlib

load_dotenv()
llm = ChatOpenAI(model_name="gpt-4-turbo")

app = Flask(__name__)

app.secret_key = "your_secret_key_here"


def get_seed_from_inputs(team1, team2, form_data):
    """Generate a consistent seed from the input parameters"""
    # Create a string combining all input parameters
    input_string = f"{team1}-{team2}"
    
    # Add all form data to input string
    for key in sorted(form_data.keys()):
        input_string += f"-{key}:{form_data[key]}"
    
    # Create a hash of the input string
    return int(hashlib.md5(input_string.encode()).hexdigest(), 16)

# Function to generate Fantasy 11 based on input players
def generate_fantasy_11(team1, team2, form_data):
    # Get all players
    all_players = get_players_from_url(team1, team2)
    
    # Generate seed from inputs
    seed = get_seed_from_inputs(team1, team2, form_data)
    
    # Set random seed for consistent selection
    random.seed(seed)
    
    # Shuffle and select players
    shuffled_players = all_players.copy()
    random.shuffle(shuffled_players)
    
    # Reset random seed
    random.seed()
    
    return shuffled_players[:11]


# Function to get justification from LLM with improved prompt
# def get_llm_justification(players):
#     try:
#         prompt = f"""
#         Analyze this fantasy cricket team selection:
#         Selected players: {', '.join(players)}
        
#         Please provide:
#         1. Overall team balance
#         2. Key players to watch
#         3. Potential performance impact
        
#         Keep the analysis brief but informative.
#         """
#         fantasy_analysis = llm.predict(prompt)
#         return fantasy_analysis
#     except Exception as e:
#         print(f"Error in LLM justification: {str(e)}")  # Debug print
#         return "Unable to generate justification at this time."

@app.route('/')
def home():
    session.clear()
    return render_template('index.html')

@app.route('/get_popular_picks', methods=['GET'])
def get_popular_picks():
    # Get team names from query parameters instead of session
    team1 = request.args.get('team1')
    team2 = request.args.get('team2')
    
    if not team1 or not team2:
        return jsonify({"error": "Please select both teams first"})
    
    players_list = get_players_from_url(team1, team2)
    return jsonify({"popular_picks": players_list[:5]})
    

@app.route('/predict', methods=['POST'])
def predict():
    try:
        team1 = request.form.get('team1')
        team2 = request.form.get('team2')

        if team1 == team2:
            return jsonify({'error': 'Please select different teams'})
        
        # Get all form data
        form_data = request.form.to_dict()
        
        fantasy_11 = generate_fantasy_11(team1, team2, form_data)
        
        return jsonify({
            'Fantasy 11': fantasy_11
        })
    except Exception as e:
        print(f"Error in predict route: {str(e)}")
        return jsonify({'error': f'An error occurred: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True)