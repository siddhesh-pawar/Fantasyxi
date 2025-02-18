from flask import Flask, render_template, request, jsonify
import random
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from scrape11 import get_playing_xi
from matches import get_players_from_url

load_dotenv()
llm = ChatOpenAI(model_name="gpt-4-turbo")

app = Flask(__name__)

Team1=""
Team2=""
# Function to generate Fantasy 11 based on input players
def generate_fantasy_11(team1,team2):
    all_players = get_players_from_url(team1,team2)
    print(all_players)
    random.shuffle(all_players)  # Shuffle to add randomness
    return all_players[:11]  # Select top 11


# Function to get justification from LLM with improved prompt
def get_llm_justification(players):
    try:
        prompt = f"""
        Analyze this fantasy cricket team selection:
        Selected players: {', '.join(players)}
        
        Please provide:
        1. Overall team balance
        2. Key players to watch
        3. Potential performance impact
        
        Keep the analysis brief but informative.
        """
        fantasy_analysis = llm.predict(prompt)
        return fantasy_analysis
    except Exception as e:
        print(f"Error in LLM justification: {str(e)}")  # Debug print
        return "Unable to generate justification at this time."

@app.route('/')
def home():
    return render_template('index.html')

# @app.route('/get_popular_picks', methods=['POST'])
# def get_popular_picks():
    

@app.route('/predict', methods=['POST'])
def predict():
    try:
        team1 = Team1= request.form.get('team1')
        team2 = Team2 = request.form.get('team2')
        
        if not team1 or not team2:
            return jsonify({'error': 'Please enter valid team names'})
        
        fantasy_11 = generate_fantasy_11(team1,team2)
        justification = get_llm_justification(fantasy_11)
        
        return jsonify({
            'Fantasy 11': fantasy_11,
            'Justification': justification
        })
    except Exception as e:
        print(f"Error in predict route: {str(e)}")  # Debug print
        return jsonify({'error': f'An error occurred: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True)