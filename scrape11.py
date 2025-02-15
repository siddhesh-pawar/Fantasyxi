import requests
from bs4 import BeautifulSoup

def get_playing_xi():
    # URL of the match playing XI page
    url = "https://www.espncricinfo.com/series/england-in-india-2024-25-1439850/india-vs-england-3rd-odi-1439906/match-playing-xi"
    
    # Send a GET request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch page, status code: {response.status_code}")
    
    # Parse the page content
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Extract player names
    players = soup.select("a[class*='ds-inline-flex'] span[class*='ds-text-tight-m']")
    player_names = []
    for player in players:
        player_names.append(player.text.strip())

    player_names=player_names[:23]
    player_names=list(set(player_names))
    return player_names

# Run the scraper
if __name__ == "__main__":
    try:
        players = get_playing_xi()
        print(players)
    except Exception as e:
        print(f"An error occurred: {e}")
