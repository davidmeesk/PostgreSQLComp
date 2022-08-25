from app import db
from app.models import Species
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
        for row in csvreader:
            # # Name   Type 1  Type 2  Total   HP  Attack  Defense Sp. Atk Sp. Def Speed   Generation  Legendary
            id = row[0]
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
            legendary = row[12]
            species = Species(
                id=id,
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
            db.session.add(species)
            db.session.commit()


if __name__ == '__main__':
    insert_pokemon_species()
