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
def get_tallest_players():
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


@bp.before_request
def before_request():
    g.start = time.time()

@bp.teardown_request
def teardown_request(exception=None):
    diff = time.time() - g.start
    print("query time: " + str(diff))
