import json
from collections import defaultdict
from database import db
from .models import HeroStats, MatchesData

HERO_DATA_DICT = {}
try:
    with open('assets/heroes.json', 'r') as f:
        heroes_list = json.load(f)
        HERO_DATA_DICT = {str(hero['id']): hero for hero in heroes_list}
except FileNotFoundError:
    print("WARNING: assets/heroes.json not found. Hero names will be unknown.")
except (TypeError, KeyError):
    print("ERROR: heroes.json is not in the expected format (a list of objects with 'id').")

UNRELEASED_HEROES = {61, 53, 48}

def calculate_filteredbatch(db_matches):
    hero_stats = get_picks_wins(db_matches)
    total_matches = len(db_matches)
    result = {}
    for hero_id, stats in hero_stats.items():
        picks = stats["picks"]
        wins = stats["wins"]
        result[hero_id] = {
            "picks": picks,
            "wins": wins,
            "winrate": (wins / picks) if picks > 0 else 0,
            "pickrate": (picks / (total_matches * 10)) if total_matches > 0 else 0
        }
    return result

def get_picks_wins(matches):
    hero_stats = defaultdict(lambda: {"picks": 0, "wins": 0})
    TEAM_MAP = {'Team0': 0, 'Team1': 1}

    for match in matches:
        winning_team_str = match.winning_team
        
        try:
            players_data = json.loads(match.players_data)
            for player in players_data:
                hero_id = player.get("hero_id")
                player_team_str = player.get("team")

                if not hero_id or player_team_str is None or hero_id in UNRELEASED_HEROES:
                    continue
                
                hero_stats[hero_id]["picks"] += 1

                player_team_int = TEAM_MAP.get(player_team_str)
                winning_team_int = TEAM_MAP.get(winning_team_str)

                if player_team_int is not None and player_team_int == winning_team_int:
                    hero_stats[hero_id]["wins"] += 1

        except (json.JSONDecodeError, TypeError):
            continue
            
    return hero_stats

def calculate_defaultbatch(db_matches):
    hero_stats = get_picks_wins(db_matches)
    total_matches = len(db_matches)
    updated_heroes = 0
    for hero_id, stats in hero_stats.items():
        hero = db.session.get(HeroStats, hero_id)
        if not hero:
            hero = HeroStats(hero_id=hero_id)
            db.session.add(hero)
        
        hero_info = HERO_DATA_DICT.get(str(hero_id), {})
        hero.hero_name = hero_info.get("name", f"Unknown Hero {hero_id}")
        
        picks = stats.get("picks", 0)
        wins = stats.get("wins", 0)
        hero.winrate = (wins / picks) if picks > 0 else 0
        hero.pickrate = (picks / (total_matches * 10)) if total_matches > 0 else 0
        hero.match_count = picks
        updated_heroes += 1

    print(f"Attempting to commit {updated_heroes} hero stat updates to the database...")
    db.session.commit()
    print(f"✅ {updated_heroes} hero stats saved to database")



if __name__ == "__main__":
    from ranklock_app import create_app
    app = create_app()
    with app.app_context():
        print("Starting hero stats calculation...")
        query = MatchesData.query.order_by(MatchesData.start_time.desc())
        matchdata = query.limit(15000).all()
        if not matchdata:
            print("No matches found in the 'matches' table ")
        else:
            print(f"Found {len(matchdata)} matches to process.")
            calculate_defaultbatch(matchdata)
            print(f"Finished processing.")