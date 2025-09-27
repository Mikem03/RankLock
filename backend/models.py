from database import db

class MatchesData(db.Model):
    __tablename__ = 'matches'
    match_id = db.Column(db.String(50), primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    winning_team = db.Column(db.Integer, nullable=False)
    average_rank = db.Column(db.Float)
    players_data = db.Column(db.Text, nullable=False)

class HeroStats(db.Model):
    __tablename__ = 'hero_stats'
    hero_id = db.Column(db.Integer, primary_key=True)
    hero_name = db.Column(db.String(50))
    pickrate = db.Column(db.Float)
    winrate = db.Column(db.Float)

class ItemStats(db.Model):
    __tablename__ = 'item_stats'
    id = db.Column(db.Integer, primary_key=True)
    hero_id = db.Column(db.Integer, db.ForeignKey('hero_stats.hero_id'))
    item_id = db.Column(db.Integer)
    item_name = db.Column(db.String(100))
    pickrate = db.Column(db.Float)
    winrate = db.Column(db.Float)

    hero = db.relationship('HeroStats', backref='items')
    print("Models defined successfully.")