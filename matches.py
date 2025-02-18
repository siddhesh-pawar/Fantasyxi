import requests
from bs4 import BeautifulSoup

# Dictionary mapping match numbers to URLs
match_urls = {
    1: "https://www.cricbuzz.com/cricket-match-squads/114960/kkr-vs-rcb-1st-match-indian-premier-league-2025",
    2: "https://www.cricbuzz.com/cricket-match-squads/114967/srh-vs-rr-2nd-match-indian-premier-league-2025",
    3: "https://www.cricbuzz.com/cricket-match-squads/114976/csk-vs-mi-3rd-match-indian-premier-league-2025",
    4: "https://www.cricbuzz.com/cricket-match-squads/114985/dc-vs-lsg-4th-match-indian-premier-league-2025",
    5: "https://www.cricbuzz.com/cricket-match-squads/114987/gt-vs-pbks-5th-match-indian-premier-league-2025",
    6: "https://www.cricbuzz.com/cricket-match-squads/114996/rr-vs-kkr-6th-match-indian-premier-league-2025",
    7: "https://www.cricbuzz.com/cricket-match-squads/115005/srh-vs-lsg-7th-match-indian-premier-league-2025",
    8: "https://www.cricbuzz.com/cricket-match-squads/115012/csk-vs-rcb-8th-match-indian-premier-league-2025",
    9: "https://www.cricbuzz.com/cricket-match-squads/115014/gt-vs-mi-9th-match-indian-premier-league-2025",
    10: "https://www.cricbuzz.com/cricket-match-squads/115021/dc-vs-srh-10th-match-indian-premier-league-2025",
    11: "https://www.cricbuzz.com/cricket-match-squads/115030/rr-vs-csk-11th-match-indian-premier-league-2025",
    12: "https://www.cricbuzz.com/cricket-match-squads/115032/mi-vs-kkr-12th-match-indian-premier-league-2025",
    13: "https://www.cricbuzz.com/cricket-match-squads/115039/lsg-vs-pbks-13th-match-indian-premier-league-2025",
    14: "https://www.cricbuzz.com/cricket-match-squads/115048/rcb-vs-gt-14th-match-indian-premier-league-2025",
    15: "https://www.cricbuzz.com/cricket-match-squads/115050/kkr-vs-srh-15th-match-indian-premier-league-2025",
    16: "https://www.cricbuzz.com/cricket-match-squads/115059/lsg-vs-mi-16th-match-indian-premier-league-2025",
    17: "https://www.cricbuzz.com/cricket-match-squads/115068/csk-vs-dc-17th-match-indian-premier-league-2025",
    18: "https://www.cricbuzz.com/cricket-match-squads/115075/pbks-vs-rr-18th-match-indian-premier-league-2025",
    19: "https://www.cricbuzz.com/cricket-match-squads/115084/kkr-vs-lsg-19th-match-indian-premier-league-2025",
    20: "https://www.cricbuzz.com/cricket-match-squads/115093/srh-vs-gt-20th-match-indian-premier-league-2025",
    21: "https://www.cricbuzz.com/cricket-match-squads/115095/mi-vs-rcb-21st-match-indian-premier-league-2025",
    22: "https://www.cricbuzz.com/cricket-match-squads/115102/pbks-vs-csk-22nd-match-indian-premier-league-2025",
    23: "https://www.cricbuzz.com/cricket-match-squads/115104/gt-vs-rr-23rd-match-indian-premier-league-2025",
    24: "https://www.cricbuzz.com/cricket-match-squads/115111/rcb-vs-dc-24th-match-indian-premier-league-2025",
    25: "https://www.cricbuzz.com/cricket-match-squads/115113/csk-vs-kkr-25th-match-indian-premier-league-2025",
    26: "https://www.cricbuzz.com/cricket-match-squads/115122/lsg-vs-gt-26th-match-indian-premier-league-2025",
    27: "https://www.cricbuzz.com/cricket-match-squads/115129/srh-vs-pbks-27th-match-indian-premier-league-2025",
    28: "https://www.cricbuzz.com/cricket-match-squads/115138/rr-vs-rcb-28th-match-indian-premier-league-2025",
    29: "https://www.cricbuzz.com/cricket-match-squads/115140/dc-vs-mi-29th-match-indian-premier-league-2025",
    30: "https://www.cricbuzz.com/cricket-match-squads/115149/lsg-vs-csk-30th-match-indian-premier-league-2025",
    31: "https://www.cricbuzz.com/cricket-match-squads/115156/pbks-vs-kkr-31st-match-indian-premier-league-2025",
    32: "https://www.cricbuzz.com/cricket-match-squads/115165/dc-vs-rr-32nd-match-indian-premier-league-2025",
    33: "https://www.cricbuzz.com/cricket-match-squads/115167/mi-vs-srh-33rd-match-indian-premier-league-2025",
    34: "https://www.cricbuzz.com/cricket-match-squads/115174/rcb-vs-pbks-34th-match-indian-premier-league-2025",
    35: "https://www.cricbuzz.com/cricket-match-squads/115176/gt-vs-dc-35th-match-indian-premier-league-2025",
    36: "https://www.cricbuzz.com/cricket-match-squads/115183/rr-vs-lsg-36th-match-indian-premier-league-2025",
    37: "https://www.cricbuzz.com/cricket-match-squads/115192/pbks-vs-rcb-37th-match-indian-premier-league-2025",
    38: "https://www.cricbuzz.com/cricket-match-squads/115201/mi-vs-csk-38th-match-indian-premier-league-2025",
    39: "https://www.cricbuzz.com/cricket-match-squads/115210/kkr-vs-gt-39th-match-indian-premier-league-2025",
    40: "https://www.cricbuzz.com/cricket-match-squads/115212/lsg-vs-dc-40th-match-indian-premier-league-2025",
    41: "https://www.cricbuzz.com/cricket-match-squads/115221/srh-vs-mi-41st-match-indian-premier-league-2025",
    42: "https://www.cricbuzz.com/cricket-match-squads/115230/rcb-vs-rr-42nd-match-indian-premier-league-2025",
    43: "https://www.cricbuzz.com/cricket-match-squads/115239/csk-vs-srh-43rd-match-indian-premier-league-2025",
    44: "https://www.cricbuzz.com/cricket-match-squads/115248/kkr-vs-pbks-44th-match-indian-premier-league-2025",
    45: "https://www.cricbuzz.com/cricket-match-squads/115255/mi-vs-lsg-45th-match-indian-premier-league-2025",
    46: "https://www.cricbuzz.com/cricket-match-squads/115257/dc-vs-rcb-46th-match-indian-premier-league-2025",
    47: "https://www.cricbuzz.com/cricket-match-squads/115266/rr-vs-gt-47th-match-indian-premier-league-2025",
    48: "https://www.cricbuzz.com/cricket-match-squads/115275/dc-vs-kkr-48th-match-indian-premier-league-2025",
    49: "https://www.cricbuzz.com/cricket-match-squads/115282/csk-vs-pbks-49th-match-indian-premier-league-2025",
    50: "https://www.cricbuzz.com/cricket-match-squads/115291/rr-vs-mi-50th-match-indian-premier-league-2025",
    51: "https://www.cricbuzz.com/cricket-match-squads/115300/gt-vs-srh-51st-match-indian-premier-league-2025",
    52: "https://www.cricbuzz.com/cricket-match-squads/115302/rcb-vs-csk-52nd-match-indian-premier-league-2025",
    53: "https://www.cricbuzz.com/cricket-match-squads/115309/kkr-vs-rr-53rd-match-indian-premier-league-2025",
    54: "https://www.cricbuzz.com/cricket-match-squads/115318/pbks-vs-lsg-54th-match-indian-premier-league-2025",
    55: "https://www.cricbuzz.com/cricket-match-squads/115327/srh-vs-dc-55th-match-indian-premier-league-2025",
    56: "https://www.cricbuzz.com/cricket-match-squads/115336/mi-vs-gt-56th-match-indian-premier-league-2025",
    57: "https://www.cricbuzz.com/cricket-match-squads/115345/kkr-vs-csk-57th-match-indian-premier-league-2025",
    58: "https://www.cricbuzz.com/cricket-match-squads/115347/pbks-vs-dc-58th-match-indian-premier-league-2025",
    59: "https://www.cricbuzz.com/cricket-match-squads/115354/lsg-vs-rcb-59th-match-indian-premier-league-2025",
    60: "https://www.cricbuzz.com/cricket-match-squads/115356/srh-vs-kkr-60th-match-indian-premier-league-2025",
    61: "https://www.cricbuzz.com/cricket-match-squads/115365/pbks-vs-mi-61st-match-indian-premier-league-2025",
    62: "https://www.cricbuzz.com/cricket-match-squads/115372/dc-vs-gt-62nd-match-indian-premier-league-2025",
    63: "https://www.cricbuzz.com/cricket-match-squads/115381/csk-vs-rr-63rd-match-indian-premier-league-2025",
    64: "https://www.cricbuzz.com/cricket-match-squads/115390/rcb-vs-srh-64th-match-indian-premier-league-2025",
    65: "https://www.cricbuzz.com/cricket-match-squads/115392/gt-vs-lsg-65th-match-indian-premier-league-2025",
    66: "https://www.cricbuzz.com/cricket-match-squads/115401/mi-vs-dc-66th-match-indian-premier-league-2025",
    67: "https://www.cricbuzz.com/cricket-match-squads/115410/rr-vs-pbks-67th-match-indian-premier-league-2025",
    68: "https://www.cricbuzz.com/cricket-match-squads/115417/rcb-vs-kkr-68th-match-indian-premier-league-2025",
    69: "https://www.cricbuzz.com/cricket-match-squads/115426/gt-vs-csk-69th-match-indian-premier-league-2025",
    70: "https://www.cricbuzz.com/cricket-match-squads/115435/lsg-vs-srh-70th-match-indian-premier-league-2025"
}


# Dictionary mapping team pairs to match numbers
match_teams = {
    1: ("Kolkata Knight Riders", "Royal Challengers Bengaluru"),
    2: ("Sunrisers Hyderabad", "Rajasthan Royals"),
    3: ("Chennai Super Kings", "Mumbai Indians"),
    4: ("Delhi Capitals", "Lucknow Super Giants"),
    5: ("Gujarat Titans", "Punjab Kings"),
    6: ("Rajasthan Royals", "Kolkata Knight Riders"),
    7: ("Sunrisers Hyderabad", "Lucknow Super Giants"),
    8: ("Chennai Super Kings", "Royal Challengers Bengaluru"),
    9: ("Gujarat Titans", "Mumbai Indians"),
    10: ("Delhi Capitals", "Sunrisers Hyderabad"),
    11: ("Rajasthan Royals", "Chennai Super Kings"),
    12: ("Mumbai Indians", "Kolkata Knight Riders"),
    13: ("Lucknow Super Giants", "Punjab Kings"),
    14: ("Royal Challengers Bengaluru", "Gujarat Titans"),
    15: ("Kolkata Knight Riders", "Sunrisers Hyderabad"),
    16: ("Lucknow Super Giants", "Mumbai Indians"),
    17: ("Chennai Super Kings", "Delhi Capitals"),
    18: ("Punjab Kings", "Rajasthan Royals"),
    19: ("Kolkata Knight Riders", "Lucknow Super Giants"),
    20: ("Sunrisers Hyderabad", "Gujarat Titans"),
    21: ("Mumbai Indians", "Royal Challengers Bengaluru"),
    22: ("Punjab Kings", "Chennai Super Kings"),
    23: ("Gujarat Titans", "Rajasthan Royals"),
    24: ("Royal Challengers Bengaluru", "Delhi Capitals"),
    25: ("Chennai Super Kings", "Kolkata Knight Riders"),
    26: ("Lucknow Super Giants", "Gujarat Titans"),
    27: ("Sunrisers Hyderabad", "Punjab Kings"),
    28: ("Rajasthan Royals", "Royal Challengers Bengaluru"),
    29: ("Delhi Capitals", "Mumbai Indians"),
    30: ("Lucknow Super Giants", "Chennai Super Kings"),
    31: ("Punjab Kings", "Kolkata Knight Riders"),
    32: ("Delhi Capitals", "Rajasthan Royals"),
    33: ("Mumbai Indians", "Sunrisers Hyderabad"),
    34: ("Royal Challengers Bengaluru", "Punjab Kings"),
    35: ("Gujarat Titans", "Delhi Capitals"),
    36: ("Rajasthan Royals", "Lucknow Super Giants"),
    37: ("Punjab Kings", "Royal Challengers Bengaluru"),
    38: ("Mumbai Indians", "Chennai Super Kings"),
    39: ("Kolkata Knight Riders", "Gujarat Titans"),
    40: ("Lucknow Super Giants", "Delhi Capitals"),
    41: ("Sunrisers Hyderabad", "Mumbai Indians"),
    42: ("Royal Challengers Bengaluru", "Rajasthan Royals"),
    43: ("Chennai Super Kings", "Sunrisers Hyderabad"),
    44: ("Kolkata Knight Riders", "Punjab Kings"),
    45: ("Mumbai Indians", "Lucknow Super Giants"),
    46: ("Delhi Capitals", "Royal Challengers Bengaluru"),
    47: ("Rajasthan Royals", "Gujarat Titans"),
    48: ("Delhi Capitals", "Kolkata Knight Riders"),
    49: ("Chennai Super Kings", "Punjab Kings"),
    50: ("Rajasthan Royals", "Mumbai Indians"),
    51: ("Gujarat Titans", "Sunrisers Hyderabad"),
    52: ("Royal Challengers Bengaluru", "Chennai Super Kings"),
    53: ("Kolkata Knight Riders", "Rajasthan Royals"),
    54: ("Punjab Kings", "Lucknow Super Giants"),
    55: ("Sunrisers Hyderabad", "Delhi Capitals"),
    56: ("Mumbai Indians", "Gujarat Titans"),
    57: ("Kolkata Knight Riders", "Chennai Super Kings"),
    58: ("Punjab Kings", "Delhi Capitals"),
    59: ("Lucknow Super Giants", "Royal Challengers Bengaluru"),
    60: ("Sunrisers Hyderabad", "Kolkata Knight Riders"),
    61: ("Punjab Kings", "Mumbai Indians"),
    62: ("Delhi Capitals", "Gujarat Titans"),
    63: ("Chennai Super Kings", "Rajasthan Royals"),
    64: ("Royal Challengers Bengaluru", "Sunrisers Hyderabad"),
    65: ("Gujarat Titans", "Lucknow Super Giants"),
    66: ("Mumbai Indians", "Delhi Capitals"),
    67: ("Rajasthan Royals", "Punjab Kings"),
    68: ("Royal Challengers Bengaluru", "Kolkata Knight Riders"),
    69: ("Gujarat Titans", "Chennai Super Kings"),
    70: ("Lucknow Super Giants", "Sunrisers Hyderabad")
}


def get_players_from_url(team1, team2):
    try:
        match_no = None
        for key, value in match_teams.items():
            if value == (team1, team2):  # Match teams in exact order
                match_no = key
                break
        
        if match_no is None:
            print("Match not found for the given teams.")
            return [], []

        url = match_urls.get(match_no)
        if not url:
            print("URL not found for the match number.")
            return [], []
        
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        left_players = soup.find_all('div', class_='cb-player-name-left')[:11]
        right_players = soup.find_all('div', class_='cb-player-name-right')[:11]

        team1_players = [div.get_text().split(' (')[0].strip() for div in left_players]
        team2_players = [div.get_text().split(' (')[0].strip() for div in right_players]

        if not team1_players and not team2_players:
            print("Could not fetch player names from the given URL.")
        else:
            players_list = team1_players + team2_players
            player_list2 = []
            for player in players_list:
                lst = player.split(" ")
                if len(lst)==2:
                    player_list2.append(player)
                else:
                    s = " ".join(lst[:2])
                    player_list2.append(s)
        return player_list2

    except Exception as e:
        print(f"Error fetching player names: {str(e)}")
        return [], []

def main():
    """Main function to get user input and fetch player lists."""
    team1 = input("Enter the first team name: ").strip()
    team2 = input("Enter the second team name: ").strip()

    player_list2 = get_players_from_url(team1, team2)
    print("\nPlayers List:", player_list2)

if __name__ == "__main__":
    main()