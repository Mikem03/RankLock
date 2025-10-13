from flask import request, jsonify
from .models import HeroStats, ItemStats

def register_routes(app):
    @app.route("/view-heroes")
    def view_heroes():
        from .services import get_filtered_heroes_logic

        min_rank = request.args.get('min_rank', type=int)
        max_rank = request.args.get('max_rank', type=int)

        if min_rank is None and max_rank is None:
            # Default, pre-calculated batch
            heroes = HeroStats.query.filter(HeroStats.winrate > 0).all()
            hero_list = [{"id": hero.hero_id, "name": hero.hero_name, "winrate": hero.winrate, "pickrate": hero.pickrate} for hero in heroes]
            return jsonify({
                "heroes": hero_list,
                "filters_applied": "False",
                "total_matches": "pre-calculated"
            })
        else:
            # Filtered batch, calling the service logic
            result = get_filtered_heroes_logic(min_rank, max_rank)
            return jsonify(result)

    @app.route("/view-items")
    def view_items():
        items = ItemStats.query.all()
        item_list = [{"id": item.item_id, "name": item.item_name, "hero_id": item.hero_id, "winrate": item.winrate, "pickrate": item.pickrate} for item in items]
        return jsonify(item_list)

    RANK_MAPPING = {
        0: "Obscurus", 1: "Initiate", 2: "Seeker", 3: "Alchemist", 4: "Arcanist",
        5: "Ritualist", 6: "Emissary", 7: "Archon", 8: "Oracle", 9: "Phantom",
        10: "Ascendant", 11: "Eternus"
    }

    @app.route("/ranks")
    def get_ranks():
        ranks = [{"rank_id": rank_id, "rank_name": rank_name} for rank_id, rank_name in RANK_MAPPING.items()]
        return jsonify(ranks)