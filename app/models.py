
from flask import current_app
from app import db

class TeamMatches(db.Model):    
    match_id = db.Column(db.String(), nullable=False, primary_key=True)
    team = db.Column(db.String(), nullable=False)
    won = db.Column(db.Boolean, nullable=False)
    points = db.Column(db.Integer, nullable=False)
    fgm = db.Column(db.Integer, nullable=False)
    fga = db.Column(db.Integer, nullable=False)
    fgp = db.Column(db.Float, nullable=False)
    tpm = db.Column(db.Integer, nullable=False)
    tpa = db.Column(db.Integer, nullable=False)
    tpp = db.Column(db.Float, nullable=False)
    ftm = db.Column(db.Integer, nullable=False)
    fta = db.Column(db.Integer, nullable=False)
    ftp = db.Column(db.Float, nullable=False)
    oreb = db.Column(db.Integer, nullable=False)
    dreb = db.Column(db.Integer, nullable=False)
    reb = db.Column(db.Integer, nullable=False)
    ast = db.Column(db.Integer, nullable=False)
    stl = db.Column(db.Integer, nullable=False)
    blk = db.Column(db.Integer, nullable=False)
    tov = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<TeamMatches {}>'.format(self.id)


class PlayersMatches(db.Model):    
    id = db.Column(db.Integer, primary_key=True)
    player = db.Column(db.String(), db.ForeignKey('players_shooting.player'), nullable=False)
    team = db.Column(db.String(), nullable=False)
    match_id = db.Column(db.String(), db.ForeignKey('team_matches.match_id'), nullable=False)
    won = db.Column(db.Boolean, nullable=False)
    points = db.Column(db.Integer, nullable=False)
    fgm = db.Column(db.Integer, nullable=False)
    fga = db.Column(db.Integer, nullable=False)
    fgp = db.Column(db.Float, nullable=False)
    tpm = db.Column(db.Integer, nullable=False)
    tpa = db.Column(db.Integer, nullable=False)
    tpp = db.Column(db.Float, nullable=False)
    ftm = db.Column(db.Integer, nullable=False)
    fta = db.Column(db.Integer, nullable=False)
    ftp = db.Column(db.Float, nullable=False)
    oreb = db.Column(db.Integer, nullable=False)
    dreb = db.Column(db.Integer, nullable=False)
    reb = db.Column(db.Integer, nullable=False)
    ast = db.Column(db.Integer, nullable=False)
    stl = db.Column(db.Integer, nullable=False)
    blk = db.Column(db.Integer, nullable=False)
    tov = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<PlayersMatches {}>'.format(self.id)


class PlayersShooting(db.Model):    
    player = db.Column(db.String(), primary_key=True)
    team = db.Column(db.String(), nullable=False)
    age = db.Column(db.Float, nullable=False)
    rar_fgm = db.Column(db.Float, nullable=False)
    rar_fga = db.Column(db.Float, nullable=False)
    rar_fgp = db.Column(db.Float, nullable=False)
    itp_fgm = db.Column(db.Float, nullable=False)
    itp_fga = db.Column(db.Float, nullable=False)
    itp_fgp = db.Column(db.Float, nullable=False)
    mrg_fgm = db.Column(db.Float, nullable=False)
    mrg_fga = db.Column(db.Float, nullable=False)
    mrg_fgp = db.Column(db.Float, nullable=False)
    lc3_fgm = db.Column(db.Float, nullable=False)
    lc3_fga = db.Column(db.Float, nullable=False)
    lc3_fgp = db.Column(db.Float, nullable=False)
    rc3_fgm = db.Column(db.Float, nullable=False)
    rc3_fga = db.Column(db.Float, nullable=False)
    rc3_fgp = db.Column(db.Float, nullable=False)
    cn3_fgm = db.Column(db.Float, nullable=False)
    cn3_fga = db.Column(db.Float, nullable=False)
    cn3_fgp = db.Column(db.Float, nullable=False)
    ab3_fgm = db.Column(db.Float, nullable=False)
    ab3_fga = db.Column(db.Float, nullable=False)
    ab3_fgp = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<PlayersShooting {}>'.format(self.player)


class PlayersInfo(db.Model):
    player = db.Column(db.String(), db.ForeignKey('players_shooting.player'), primary_key=True)
    team = db.Column(db.String())
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)

    def __repr__(self):
        return '<PlayersInfo {}>'.format(self.player)
