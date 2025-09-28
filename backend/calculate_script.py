import json
from collections import defaultdict

def calculate_filteredbatch(db_matches):
    hero_stats = get_picks_wins(db_matches)
    total_matches = len(db_matches)

    result = {}
    for hero_id, stats in hero_stats.items():
        picks = stats["picks"]
        wins = stats["wins"]
        winrate = wins / picks if picks > 0 else 0  # Keep as decimal (0.0-1.0)
        pickrate = picks / (total_matches * 10) if total_matches > 0 else 0  # Keep as decimal
        
        result[hero_id] = {
            "picks": picks,
            "wins": wins,
            "winrate": winrate,
            "pickrate": pickrate
        }
    
    return result

def get_picks_wins(matches):
    hero_stats = defaultdict(lambda: {"picks": 0, "wins": 0})

    for match in matches:
        winning_team = match.winning_team
        players_data = json.loads(match.players_data)

        for player in players_data:
            hero_id = player["hero_id"]
            player_team = player["team"]

            hero_stats[hero_id]["picks"] += 1

            if player_team == winning_team:
                hero_stats[hero_id]["wins"] += 1

    return hero_stats

def calculate_defaultbatch(db_matches):
    from database import db
    from models import HeroStats

    hero_stats = get_picks_wins(db_matches)

    updated_heroes = 0
    for hero_id, stats in hero_stats.items():
        picks = stats["picks"]
        wins = stats["wins"]
        winrate = (wins / picks) * 100 if picks > 0 else 0
        pickrate = (picks / (len(db_matches) * 10)) * 100

        print(f"Hero {hero_id}: Pickrate = {pickrate:.2f}%, Winrate = {winrate:.2f}%")

        # Update or create hero stats in database
        hero = HeroStats.query.filter_by(hero_id=hero_id).first()
        if hero:
            hero.pickrate = pickrate
            hero.winrate = winrate
            print(f"Updated existing hero {hero.hero_name} (ID: {hero_id})")
        else:
            hero = HeroStats(
                hero_id=hero_id,
                hero_name=f"Hero_{hero_id}",
                pickrate=pickrate,
                winrate=winrate
            )
            db.session.add(hero)
            print(f"Created new hero entry for {hero.hero_name}")
        updated_heroes += 1
    db.session.commit()
    print(f"{updated_heroes} hero stats saved to database")


if __name__ == "__main__":
    from app import app
    from models import MatchesData
    with app.app_context():
        print("Starting hero stats calculation...")

        query = MatchesData.query.order_by(MatchesData.start_time.desc())
        matchdata = query.limit(15000).all()

        calculate_defaultbatch(matchdata)

        print(f"Finished. Matches processed: {len(matchdata)}")
