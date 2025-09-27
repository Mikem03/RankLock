import json
import requests 
from flask import Flask
from database import db
from models import MatchesData
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ranklock.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def fetch_matches(limit=10000):    
    try:
        matches = requests.get(
            f"https://api.deadlock-api.com/v1/matches/metadata?limit={limit}&order_by=start_time&order_direction=desc&include_player_info=true"
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
                team1rank = match["average_badge_team0"]
                team2rank = match["average_badge_team1"]
                if team1rank is None and team2rank is None:
                    avg_rank = None
                else:
                    avg_rank = (team1rank + team2rank) / 2.0

                new_match = MatchesData(
                    match_id=match_id,
                    start_time=start_time,
                    winning_team=match["winning_team"],
                    average_rank=avg_rank,
                    players_data=json.dumps(match["players"])
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
    print("Starting daily match fetch...")
    
    with app.app_context():
        db.create_all() 
    
    success = fetch_matches(limit=10000)
    
    if success:
        print("Daily match fetch completed successfully!")
    else:
        print("Daily match fetch failed!")