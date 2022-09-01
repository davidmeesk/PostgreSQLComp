from app import db, create_app
from app.models import Species, Pokemon, Trainer
from datetime import datetime
import sqlalchemy
import csv

def feet_and_inches_to_cm(feet, inches):
    return int(round(feet*30.48 + inches*2.54))

def lbs_to_kg(lbs):
    return int(round(lbs * 453.592 / 1000))

def insert_pokemon_species():
    rows = []
    with open("data/pokedex.csv", 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        count = 1
        for row in csvreader:
            # # Name   Type 1  Type 2  Total   HP  Attack  Defense Sp. Atk Sp. Def Speed   Generation  Legendary
            id = count
            dex = row[0]
            name = row[1]
            type1 = row[2]
            type2 = row[3]
            HP = row[5]
            attack = row[6]
            defense = row[7]
            sp_atk = row[8]
            sp_def = row[9]
            speed = row[10]
            gen = row[11]
            legendary = True if row[12] == 'True' else False
            species = Species(
                id=id,
                dex=dex,
                name=name,
                type1=type1,
                type2=type2,
                HP=HP,
                attack=attack,
                defense=defense,
                sp_atk=sp_atk,
                sp_def=sp_def,
                speed=speed,
                gen=gen,
                legendary=legendary,
            )
            count += 1
            db.session.add(species)
            db.session.commit()

def insert_trainers():
    rows = []
    with open("data/trainers.csv", 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            id = row[0]
            name = row[1]
            trainer = Trainer(
                id=id,
                name=name,
            )
            db.session.add(trainer)
            db.session.commit()

def insert_pokemon():
    rows = []
    with open("data/pokemon.csv", 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        count = 1
        for row in csvreader:
            id = count
            species_id = 1
            trainer_id = row[0]
            place = row[1]
            species_name = row[2]
            level = row[3]
            pokemon = Pokemon(
                id=id,
                species_id=species_id,
                trainer_id=trainer_id,
                place=place,
                species_name=species_name,
                level=level,
            )
            count += 1
            db.session.add(pokemon)
            db.session.commit()


if __name__ == '__main__':
    app = create_app()
    app.app_context().push()
    db.create_all()
    insert_pokemon_species()
    insert_trainers()
    insert_pokemon()
    
