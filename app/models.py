
from flask import current_app
from app import db

class Species(db.Model):    
    id = db.Column(db.String(), nullable=False, primary_key=True)
    dex = db.Column(db.String(), nullable=False)
    name = db.Column(db.String(), nullable=False)
    type1 = db.Column(db.String(), nullable=False)
    type2 = db.Column(db.String(), nullable=True)
    HP = db.Column(db.Integer, nullable=False)
    attack = db.Column(db.Integer, nullable=False)
    defense = db.Column(db.Integer, nullable=False)
    sp_atk = db.Column(db.Integer, nullable=False)
    sp_def = db.Column(db.Integer, nullable=False)
    speed = db.Column(db.Integer, nullable=False)
    gen = db.Column(db.Integer, nullable=False)
    legendary = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return '<Species {}>'.format(self.id)

class Trainer(db.Model):
    id = db.Column(db.String(), nullable=False, primary_key=True)
    name = db.Column(db.String(), nullable=False)

class Pokemon(db.Model):
    id = db.Column(db.String(), nullable=False, primary_key=True)
    species_id = db.Column(db.String(), db.ForeignKey('species.id'), nullable=False)
    trainer_id = db.Column(db.String(), db.ForeignKey('trainer.id'), nullable=False)
    place = db.Column(db.Integer, nullable=False)
    species_name = db.Column(db.String(), nullable=False)
    level = db.Column(db.Integer, nullable=False)


