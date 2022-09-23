from flask import current_app, request, g
from app import db
from app.api import bp
from app.models import Species
import numpy as np 
import json
import time

@bp.route('/adjust', methods=['GET'])
def set_pokemon():
    results = db.engine.execute("""
        UPDATE pokemon
            SET species_id = S.id
        FROM species S
        WHERE pokemon.species_name = S.name; 
    """)
    results2 = db.engine.execute("""
        ALTER TABLE pokemon
        DROP COLUMN species_name; 
    """)
    response = {
        }
    return json.dumps(response)

# pokemons

@bp.route('/pokedex', methods=['GET'])
def get_pokedex():
    results = db.engine.execute("""
        SELECT *
        FROM species
    """)
    response = []
    for result in results:
        response.append({
            "id":result[0],
            "dex":result[1],
            "name":result[2],
            "type1":result[3],
            "type2":result[4],
            "HP":result[5],
            "attack":result[6],
            "defense":result[7],
            "sp_atk":result[8],
            "sp_def":result[9],
            "speed":result[10],
            "gen":result[11],
            "legendary":result[12],
        })
    return json.dumps(response)

@bp.route('/stats', methods=['GET'])
def get_stats():
    results = db.engine.execute("""
        SELECT POK.id, POK.trainer_id, POK.place, POK.level, SP.dex, SP.name, SP.type1, SP.type2, SP.\"HP\", SP.attack, SP.defense, SP.sp_atk, SP.sp_def, SP.speed
        FROM species SP
        LEFT JOIN pokemon POK
        ON SP.id = POK.species_id
        ORDER BY dex ASC
    """)
    response = []
    for result in results:
        response.append({
            "id":result[0],
            "trainer_id":result[1],
            "place":result[2],
            "level":result[3],
            "dex":result[4],
            "name":result[5],
            "type1":result[6],
            "type2":result[7],
            "HP":result[8],
            "attack":result[9],
            "defense":result[10],
            "sp_atk":result[11],
            "sp_def":result[12],
            "speed":result[13],
        })
    return json.dumps(response)


@bp.before_request
def before_request():
    g.start = time.time()

@bp.teardown_request
def teardown_request(exception=None):
    diff = time.time() - g.start
    print("query time: " + str(diff))

@bp.route('/legendaries', methods=['GET'])
def legendaries():
    results = db.engine.execute("""
        SELECT *
        FROM species
        WHERE legendary = true
    """)
    response = []
    for result in results:
        response.append({
            "id":result[0],
            "dex":result[1],
            "name":result[2],
            "type1":result[3],
            "type2":result[4],
            "HP":result[5],
            "attack":result[6],
            "defense":result[7],
            "sp_atk":result[8],
            "sp_def":result[9],
            "speed":result[10],
            "gen":result[11],
            "legendary":result[12],
        })
    return json.dumps(response)