import os
import json
from flask import Flask, request, send_from_directory, jsonify
from flask_cors import CORS
from database import db
from models import HeroStats, ItemStats, MatchesData
from calculate_script import calculate_filteredbatch # type: ignore

app = Flask(__name__, static_folder='../frontend/dist')
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ranklock.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/api/message')
def get_message():
    return {"message": "View winrates and pickrates for Deadlock, and filter by rank!"}

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_static(path):
     if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
     else:
        return send_from_directory(app.static_folder, 'index.html')  
     
UNRELEASED_HEROES = {"Trapper", "Kali", 
                     "Gunslinger", "The Boss", 
                     "Tokamak", "Wrecker", 
                     "Rutger", "Thumper", 
                     "Fathom", "Cadence",
                     "Bomber", "Shield Guy",
                     "Vandal", "Raven",
                     "Venator", "Boho",
                     "Skyrunner", "Swan",
                     "Druid", "Graf", "Fortuna"
                     }

@app.route("/heroes")
def list_heroes():
    try:
        with open(os.path.join("assets", "heroes.json"), "r") as f:
            heroes = json.load(f)

        heroes_added = 0
        for hero in heroes:
            if hero["name"] in UNRELEASED_HEROES:
                continue
            existing_hero = HeroStats.query.filter_by(hero_id=hero["id"]).first()
            if not existing_hero:
                new_hero = HeroStats(
                    hero_id=hero["id"],
                    hero_name=hero["name"],
                    pickrate=0.0,  
                    winrate=0.0
                )
                db.session.add(new_hero)
                heroes_added += 1

        db.session.commit()
        return jsonify({"message": f"Added heroes data"})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500   

@app.route("/items")
def list_items():
    try:
        with open(os.path.join("assets", "items.json"), "r") as f:
            items = json.load(f)

        for item in items:
            existing_item = ItemStats.query.filter_by(
                item_id=item["id"], 
                hero_id=0
            ).first()
            
            if not existing_item:
                new_item = ItemStats(
                    hero_id=0,  
                    item_id=item["id"],
                    item_name=item["name"],
                    pickrate=0.0, 
                    winrate=0.0
                )
                db.session.add(new_item)
                items_added += 1

        db.session.commit()
        return jsonify({"message": f"Successfully processed items data"})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500  

@app.route("/init-db")
def init_database():
    try:
        db.create_all()
        return jsonify({"message": "Database tables created successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/view-heroes")
def view_heroes():
    min_rank = request.args.get('min_rank', type=int)
    max_rank = request.args.get('max_rank', type=int)

    ### Default batch
    if min_rank is None and max_rank is None:
        heroes = HeroStats.query.filter(HeroStats.winrate > 0).all()
        hero_list = [{"id": hero.hero_id, 
                      "name": hero.hero_name, 
                      "winrate": hero.winrate, 
                      "pickrate": hero.pickrate
        } for hero in heroes]
        return jsonify({
            "heroes": hero_list,
            "filters_applied": "False",
            "total_matches": "pre-calculated"
        })
    ### Filtered batch
    else:
        return get_filtered_heroes(min_rank, max_rank)

def get_filtered_heroes(min_rank=None, max_rank=None, match_limit=25000):
    matches_query = MatchesData.query.order_by(MatchesData.start_time.desc())
    if min_rank is not None:
        matches_query = matches_query.filter(MatchesData.average_rank >= min_rank)
    if max_rank is not None:
        matches_query = matches_query.filter(MatchesData.average_rank <= max_rank)

    filtered_matches = matches_query.limit(match_limit).all()

    hero_stats = calculate_filteredbatch(filtered_matches)
    final_hero_list = []
    for hero_id, stats in hero_stats.items():
        hero = HeroStats.query.get(hero_id)
        stats["name"] = hero.hero_name if hero else f"Hero {hero_id}"
        stats["id"] = hero_id 
        final_hero_list.append(stats)

    return jsonify({
        "heroes": final_hero_list,
        "filters_applied": "True",
        "total_matches": len(filtered_matches)
    })

@app.route("/view-items")
def view_items():
    items = ItemStats.query.all()
    item_list = [{"id": item.item_id, "name": item.item_name, "hero_id": item.hero_id, "winrate": item.winrate, "pickrate": item.pickrate} for item in items]
    return jsonify(item_list)

RANK_MAPPING = {
    0: "Obscurus",
    1: "Initiate", 
    2: "Seeker",
    3: "Alchemist",
    4: "Arcanist",
    5: "Ritualist",
    6: "Emissary",
    7: "Archon",
    8: "Oracle",
    9: "Phantom",
    10: "Ascendant",
    11: "Eternus"
}

@app.route("/ranks")
def get_ranks():
    ranks = [{"rank_id": rank_id, "rank_name": rank_name} for rank_id, rank_name in RANK_MAPPING.items()]
    return jsonify(ranks)


@app.route("/images/<path:filename>")
def get_image(filename):
    return send_from_directory("assets/hero_icons", filename)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(debug=True)
