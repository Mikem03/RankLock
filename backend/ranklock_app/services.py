from .models import HeroStats, MatchesData

def get_filtered_heroes_logic(min_rank=None, max_rank=None, match_limit=25000):
    """
    Queries matches, calculates hero stats, and returns a dictionary.
    This function does NOT return a JSON response.
    """
    from .calculate_script import calculate_filteredbatch

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

    return {
        "heroes": final_hero_list,
        "filters_applied": "True",
        "total_matches": len(filtered_matches)
    }