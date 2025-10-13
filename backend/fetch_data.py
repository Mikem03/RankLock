import json
import requests 
import sys
from ranklock_app import create_app
from database import db
from ranklock_app.models import MatchesData
from datetime import datetime

app = create_app()

def fetch_matches(limit=10000):    
    try:
        matches = requests.get(
            f"https://api.deadlock-api.com/v1/matches/metadata?limit={limit}&order_direction=desc&min_average_badge=1&include_player_info=true"
        ).json()
        
        print(f"Retrieved {len(matches)} matches from API")
        
        with app.app_context():
            new_matches = 0
            duplicate_matches = 0
            
            for match in matches:
                match_id = match["match_id"]

                existing = MatchesData.query.filter_by(match_id=match_id).first()
                if existing:
                    duplicate_matches += 1
                    continue

                start_time = datetime.strptime(match["start_time"], "%Y-%m-%d %H:%M:%S")
                team1rank = match.get("average_badge_team0") or 0
                team2rank = match.get("average_badge_team1") or 0
                avg_rank = (team1rank + team2rank) / 2.0

                match_items = {}
                for player in match.get("players", []):
                    account_id = player.get("account_id")
                    items = player.get("items", [])
                    if account_id:
                        match_items[str(account_id)] = items

                new_match = MatchesData(
                    match_id=match_id,
                    start_time=start_time,
                    winning_team=match["winning_team"],
                    average_rank=avg_rank,
                    players_data=json.dumps(match["players"]),
                    items_data=json.dumps(match_items)
                )
                db.session.add(new_match)
                new_matches += 1
            
            db.session.commit()

            total_matches = MatchesData.query.count()
            print(f"Added {new_matches} new matches")
            print(f"Skipped {duplicate_matches} duplicate matches")
            print(f"Total matches in database: {total_matches}")
            
    except Exception as e:
        print(f"Error fetching matches: {e}")
        return False
    
    return True

if __name__ == "__main__":
    with app.app_context():
        if len(sys.argv) > 1 and sys.argv[1] == 'fetch':
            fetch_matches()
        else:
            print("Please provide a command. Usage: python manage_data.py fetch")