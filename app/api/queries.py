from flask import current_app, request
from app import db
from app.api import bp
from app.models import PlayersInfo
import numpy as np 
import json

# JOGADORES + ALTOS

@bp.route('/tallest', methods=['GET'])
def get_tallest_players():
    results = db.engine.execute("""
        SELECT player, height
        FROM players_info
        ORDER BY height DESC
        LIMIT 1
    """)
    for result in results:
        response = {
            "name": result[0],
            "height": result[1] 
        }
    return json.dumps(response)

# JOGADORES QUE + PONTUAM

@bp.route('/playersStatsFromTeam', methods=['GET'])
def get_players_stats_from_team():
    args = request.args
    team = args['team']
    stat = args['stat']
    results = db.engine.execute(f"""
        SELECT player, SUM({stat}) AS total
        FROM players_matches
        WHERE team='{team}'
        GROUP BY player
        ORDER BY total DESC
    """)
    response = []
    for result in results:
        response.append({
            "x": result[0], # player
            "y": result[1]  # points
        })
    return json.dumps(response)

# TIMES QUE + PONTUAM

@bp.route('/teamsMostPoints', methods=['GET'])
def get_teams_most_points():
    results = db.engine.execute(f"""
        SELECT team, SUM(points) AS totalPoints
        FROM team_matches
        GROUP BY team
        ORDER BY totalPoints DESC
    """)
    response = []
    for result in results:
        response.append({
            "team": result[0],
            "totalPoints": result[1] 
        })
    return json.dumps(response)

# JOGADORES QUE + FAZEM ASSISTÊNCIAS

@bp.route('/playersMostAssists', methods=['GET'])
def get_players_most_assists():
    args = request.args
    num = args['num']
    results = db.engine.execute(f"""
        SELECT player, SUM(ast) AS totalAssists
        FROM players_matches
        GROUP BY player
        ORDER BY totalAssists DESC
        LIMIT {num}
    """)
    response = []
    for result in results:
        response.append({
            "player": result[0],
            "totalAssists": result[1] 
        })
    return json.dumps(response)

# TIMES QUE + FAZEM ASSISTÊNCIAS

@bp.route('/teamsMostAssists', methods=['GET'])
def get_teams_most_assists():
    results = db.engine.execute(f"""
        SELECT team, SUM(ast) AS totalAssists
        FROM team_matches
        GROUP BY team
        ORDER BY totalAssists DESC
    """)
    response = []
    for result in results:
        response.append({
            "team": result[0],
            "totalAssists": result[1] 
        })
    return json.dumps(response)

# JOGADORES COM MELHOR APROVEITAMENTO EM LANCES LIVRES

@bp.route('/playersBestFreeThrow', methods=['GET'])
def get_players_best_free_throw():
    args = request.args
    num = args['num']
    minFTA = args['minFTA']
    results = db.engine.execute(f"""
        SELECT player, CAST(ROUND(SUM(ftm) * 100.0/NULLIF(SUM(fta), 0), 2) AS FLOAT) AS freeThrowPercent, SUM(fta) AS nFreeThrows, SUM(ftm) AS nFreeThrowsScored
        FROM players_matches
        GROUP BY player
        HAVING SUM(fta) >= {minFTA}
        ORDER BY freeThrowPercent DESC, nFreeThrowsScored DESC
        LIMIT {num}
    """)
    response = []
    for result in results:
        response.append({
            "player": result[0],
            "freeThrowPercent": result[1],
            "nFreeThrows": result[2],
            "nFreeThrowsScored": result[3]
        })
    return json.dumps(response)

# TIMES QUE + FAZEM ARREMESSOS DE 3 PONTOS

@bp.route('/teamsMost3Points', methods=['GET'])
def get_teams_most_3_points():
    results = db.engine.execute(f"""
        SELECT team, SUM(tpa) AS total3Points
        FROM team_matches
        GROUP BY team
        ORDER BY total3Points DESC
    """)
    response = []
    for result in results:
        response.append({
            "team": result[0],
            "total3Points": result[1] 
        })
    return json.dumps(response)

# TIMES COM MELHOR APROVEITAMENTO EM ARREMESSOS DE 3 PONTOS

@bp.route('/teamsBest3Points', methods=['GET'])
def get_teams_best_3_points():
    results = db.engine.execute(f"""
        SELECT team, CAST(ROUND(SUM(tpm) * 100.0/NULLIF(SUM(tpa), 0), 2) AS FLOAT) AS ThreePointPercent, SUM(tpa) AS n3PointsAttempted, SUM(tpm) AS n3PointsScored
        FROM team_matches
        GROUP BY team
        ORDER BY ThreePointPercent DESC, n3PointsScored DESC
    """)
    response = []
    for result in results:
        response.append({
            "team": result[0],
            "3PointPercent": result[1],
            "n3PointsAttempted": result[2],
            "n3PointsScored": result[3]
        })
    return json.dumps(response)

# JOGADORES COM MELHOR APROVEITAMENTO EM ARREMESSOS DE 3 PONTOS

@bp.route('/playersBest3Points', methods=['GET'])
def get_players_best_3_points():
    args = request.args
    num = args['num']
    minTPA = args['minTPA']
    results = db.engine.execute(f"""
        SELECT player, CAST(ROUND(SUM(tpm) * 100.0/NULLIF(SUM(tpa), 0), 2) as FLOAT) AS ThreePointPercent, SUM(tpa) AS n3PointsAttempted, SUM(tpm) AS n3PointsScored
        FROM players_matches
        GROUP BY player
        HAVING SUM(tpa) >= {minTPA}
        ORDER BY ThreePointPercent DESC, n3PointsScored DESC
        LIMIT {num}
    """)
    response = []
    for result in results:
        response.append({
            "player": result[0],
            "3PointPercent": result[1],
            "n3PointsAttempted": result[2],
            "n3PointsScored": result[3]
        })
    return json.dumps(response)

# JOGADORES COM MAIS REBOTES

@bp.route('/teamsMostRebounds', methods=['GET'])
def get_teams_most_rebounds():
    args = request.args
    num = args['num']
    results = db.engine.execute(f"""
        SELECT team, SUM(reb) AS totalRebounds
        FROM team_matches
        GROUP BY team
        ORDER BY totalRebounds DESC
        LIMIT {num}
    """)
    response = []
    for result in results:
        response.append({
            "team": result[0],
            "totalRebounds": result[1] 
        })
    return json.dumps(response)

# TIMES COM MAIS BLOQUEIOS

@bp.route('/teamsMostBlocks', methods=['GET'])
def get_teams_most_blocks():
    args = request.args
    num = args['num']
    results = db.engine.execute(f"""
        SELECT team, SUM(blk) AS totalBlocks
        FROM team_matches
        GROUP BY team
        ORDER BY totalBlocks DESC
        LIMIT {num}
    """)
    response = []
    for result in results:
        response.append({
            "team": result[0],
            "totalBlocks": result[1] 
        })
    return json.dumps(response)

# JOGADORES COM MAIS BLOQUEIOS

@bp.route('/playersMostBlocks', methods=['GET'])
def get_players_most_blocks():
    args = request.args
    num = args['num']
    results = db.engine.execute(f"""
        SELECT player, SUM(blk) AS totalBlocks
        FROM players_matches
        GROUP BY player
        ORDER BY totalBlocks DESC
        LIMIT {num}
    """)
    response = []
    for result in results:
        response.append({
            "player": result[0],
            "totalBlocks": result[1] 
        })
    return json.dumps(response)

# TIMES QUE MAIS VENCEM EM CASA

@bp.route('/teamsWinHome', methods=['GET'])
def get_teams_wins_home():
    results = db.engine.execute(f"""
        SELECT team, COUNT(case when won then 1 else null end) AS totalHomeWins, COUNT(case when NOT won then 1 else null end) AS totalHomeLosses
        FROM team_matches
        WHERE match_id LIKE CONCAT(team, \' vs.%%\')
        GROUP BY team
        ORDER BY totalHomeWins DESC
    """)
    response = []
    for result in results:
        response.append({
            "team": result[0],
            "totalHomeWins": result[1],
            "totalHomeLosses": result[2]
        })
    return json.dumps(response)

# ARREMESSOS DE JOGADORES MAIS ALTOS QUE A MÊDIA

@bp.route('/playersShootingTallerThanAvg', methods=['GET'])
def  players_shooting_taller_than_avg():
    args = request.args
    shootingStat = args['shootingStat']
    results = db.engine.execute(f"""
        SELECT players_shooting.player, height, (height > (SELECT AVG(height) FROM players_info)) as isTallerThanAvg
        FROM players_shooting
        INNER JOIN players_info
        ON players_shooting.player = players_info.player
        WHERE {shootingStat} > (SELECT AVG({shootingStat}) FROM players_shooting)
        ORDER BY {shootingStat} DESC
""")
    response = []
    for result in results:
        response.append({
            "player": result[0],
            "height": result[1],
            "isTallerThanAvg": result[2]
        })
    return json.dumps(response)

# ARREMESSOS DE JOGADORES MAIS PESADOS QUE A MÊDIA

@bp.route('/playersShootingHeavierThanAvg', methods=['GET'])
def  players_shooting_heavier_than_avg():
    args = request.args
    shootingStat = args['shootingStat']
    results = db.engine.execute(f"""
        SELECT players_shooting.player, weight, (weight > (SELECT AVG(weight) FROM players_info)) as isHeavierThanAvg
        FROM players_shooting
        INNER JOIN players_info
        ON players_shooting.player = players_info.player
        WHERE {shootingStat} > (SELECT AVG({shootingStat}) FROM players_shooting)
        ORDER BY {shootingStat} DESC
""")
    response = []
    for result in results:
        response.append({
            "player": result[0],
            "weight": result[1],
            "isHeavierThanAvg": result[2]
        })
    return json.dumps(response)

# TIMES COM MELHOR APROVEITAMENTO EM UM TIPO DE ARREMESSO

@bp.route('/teamsBestShooting', methods=['GET'])
def get_teams_best_shooting():
    args = request.args
    shootingZone = args['shootingZone']
    results = db.engine.execute(f"""
        SELECT team, CAST(to_char(SUM({shootingZone}_fgm) * 100.0/NULLIF(SUM({shootingZone}_fga), 0), 'FM999999999.00') AS FLOAT) AS shootingTypePercent, CAST(to_char(SUM({shootingZone}_fga), 'FM999999999.00') AS FLOAT) AS shootingTypeAttempted, CAST(to_char(SUM({shootingZone}_fgm), 'FM999999999.00') AS FLOAT) AS shootingTypeScored
        FROM players_shooting
        GROUP BY team
        ORDER BY shootingTypePercent DESC, shootingTypeScored DESC
    """)
    response = []
    for result in results:
        response.append({
            "team": result[0],
            "shootingTypePercent": result[1],
            "shootingTypeAttempted": result[2],
            "shootingTypeScored": result[3]
        })
    return json.dumps(response)

# JOGADORES COM MELHOR APROVEITAMENTO EM UM TIPO DE ARREMESSO

@bp.route('/playersBestShooting', methods=['GET'])
def get_players_best_shooting():
    args = request.args
    shootingZone = args['shootingZone']
    minShots = args['minShots']
    num = args['num']
    results = db.engine.execute(f"""
        SELECT player, CAST(to_char(SUM({shootingZone}_fgm) * 100.0/NULLIF(SUM({shootingZone}_fga), 0), 'FM999999999.00') AS FLOAT) AS shootingTypePercent, CAST(to_char(SUM({shootingZone}_fga), 'FM999999999.00') AS FLOAT) AS shootingTypeAttempted, CAST(to_char(SUM({shootingZone}_fgm), 'FM999999999.00') AS FLOAT) AS shootingTypeScored
        FROM players_shooting
        GROUP BY player
        HAVING CAST(to_char(SUM({shootingZone}_fga), 'FM999999999.00') AS FLOAT) > 0 AND CAST(to_char(SUM({shootingZone}_fga), 'FM999999999.00') AS FLOAT) >= {minShots}
        ORDER BY shootingTypePercent DESC, shootingTypeScored DESC
        LIMIT {num}
    """)
    response = []
    for result in results:
        response.append({
            "player": result[0],
            "shootingTypePercent": result[1],
            "shootingTypeAttempted": result[2],
            "shootingTypeScored": result[3]
        })
    return json.dumps(response)

# JOGADORES COM MAIS ACERTOS EM ARREMESSOS

@bp.route('/playersMVP', methods=['GET'])
def get_players_mvp():
    results = db.engine.execute(f"""
        SELECT team, player, (rar_fgm + itp_fgm + mrg_fgm + lc3_fgm + rc3_fgm + cn3_fgm + ab3_fgm) as totalShotsMade
        FROM players_shooting
        GROUP BY team, player
        ORDER BY totalShotsMade DESC
        LIMIT 10
    """)
    response = []
    for result in results:
        response.append({
            "team": result[0],
            "player": result[1],
            "totalShotsMade": result[2]
        })
    return json.dumps(response)

# VITÓRIAS DE TIMES COM JOGADORES COM MAIS ACERTOS EM ARREMESSOS

@bp.route('/teamsWithMVP', methods=['GET'])
def get_teams_mvp():
    results = db.engine.execute(f"""
        SELECT team, SUM(case when won then 1 else null end) as numberOfWins
        FROM team_matches
        WHERE team IN (SELECT team FROM players_shooting ORDER BY (rar_fgm + itp_fgm + mrg_fgm + lc3_fgm + rc3_fgm + cn3_fgm + ab3_fgm) DESC LIMIT 10)
        GROUP BY team
        ORDER BY numberOfWins DESC
    """)
    response = []
    for result in results:
        response.append({
            "team": result[0],
            "numberOfWins": result[1]
        })
    return json.dumps(response)

# VITÓRIAS DE TIMES COM MELHOR APROVEITAMENTO EM UMA JOGADA

@bp.route('/teamsWinMoves', methods=['GET'])
def get_teams_win_moves():
    args = request.args
    move = args['move']
    results = db.engine.execute(f"""
        SELECT team, CAST(ROUND(AVG({move}), 2) AS FLOAT) AS total_{move}, SUM(case when won then 1 else null end) as numberOfWins
        FROM team_matches
        GROUP BY team
        ORDER BY total_{move} DESC
    """)
    response = []
    for result in results:
        response.append({
            "team": result[0],
            f'total_{move}': result[1],
            "numberOfWins": result[2]
        })
    return json.dumps(response)

# JOGADORES COM MAIOR PORCENTAGEM DE 3 PONTOS

@bp.route('/playersBest3PointsPercentage', methods=['GET'])
def get_players_best_3_points_percentage():
    args = request.args
    minPoints = args['minPoints']
    num = args['num']
    results = db.engine.execute(f"""
        SELECT player, team, CAST(to_char(SUM(tpm) * 3 * 100.0/NULLIF(SUM(points), 0), 'FM999999999.00') AS FLOAT) AS threePointsPerc, SUM(points) AS totalPoints, SUM(tpm)*3 AS total3Points
        FROM players_matches
        GROUP BY player, team
        HAVING SUM(points) >= 3 AND SUM(points) >= {minPoints}
        ORDER BY threePointsPerc DESC
        LIMIT {num}
    """)
    response = []
    for result in results:
        response.append({
            "player": result[0],
            "team": result[1],
            "threePointsPerc": result[2],
            "totalPoints": result[3],
            "total3Points": result[4]
        })
    return json.dumps(response)

# MÉDIA DE PONTOS DOS JOGADORES POR PARTIDA

@bp.route('/playersAveragePoints', methods=['GET'])
def get_players_average_points():
    args = request.args
    num = args['num']
    results = db.engine.execute(f"""
        SELECT player, team, CAST(ROUND(CAST(AVG(points) AS NUMERIC), 2) AS FLOAT) AS averagePoints
        FROM players_matches
        GROUP BY player, team
        ORDER BY AVG(points) DESC
        LIMIT {num}
    """)
    response = []
    for result in results:
        response.append({
            "player": result[0],
            "team": result[1],
            "averagePoints": result[2]
        })
    return json.dumps(response)

# MÉDIA DE IDADE DOS TIMES E SUA PORCENTAGEM DE VITÓRIAS

@bp.route('/teamsAgeWins', methods=['GET'])
def get_teams_age_wins():
    results = db.engine.execute("""
        SELECT tm.team, ps.playerAge as averageAge, COUNT(tm.won) as nMatches, COUNT(case when tm.won then 1 else null end) as nWins, CAST(ROUND(CAST(COUNT(case when tm.won then 1 else null end) AS NUMERIC)/CAST(COUNT(tm.won) AS NUMERIC)*100.0, 2) AS FLOAT) AS percentWins
        FROM team_matches tm
        INNER JOIN 
            (SELECT team, CAST(ROUND(CAST(AVG(age) AS NUMERIC), 2) AS FLOAT) as playerAge FROM players_shooting GROUP BY team) ps 
            ON tm.team = ps.team     		
        GROUP BY tm.team, ps.playerAge
        ORDER BY ps.playerAge DESC
    """)
    response = []
    for result in results:
        response.append({
            "team": result[0],
            "averageAge": result[1],
            "nMatches": result[2],
            "nWins": result[3],
            "percentWins": result[4]
        })
    return json.dumps(response)

# PORCENTAGEM DE VITÓRIAS DE JOGADORES ESPECIALIZADOS EM UM ARREMESSO

@bp.route('/playersShootingWins', methods=['GET'])
def  get_players_shooting_wins():
    args = request.args
    shootingZone = args['shootingZone']
    minShots = args['minShots']
    num = args['num']
    results = db.engine.execute(f"""
        SELECT ps.player, ps.team, ps.{shootingZone}_fgp as percentShotsMade, pm.numberOfMatches as nMatches, pm.numberOfWins as nWins, CAST(ROUND(CAST(pm.numberOfWins AS NUMERIC)/CAST(pm.numberOfMatches AS NUMERIC)*100.0, 2) AS FLOAT) AS percentWins
        FROM players_shooting ps
        INNER JOIN 
            (SELECT player, COUNT(won) as numberOfMatches, COUNT(case when won then 1 else null end) as numberOfWins FROM players_matches GROUP BY player) pm
            ON ps.player = pm.player  
        WHERE ps.{shootingZone}_fga > {minShots}
        GROUP BY ps.player, pm.numberOfMatches, pm.numberOfWins
        ORDER BY percentShotsMade DESC
        LIMIT {num}
""")
    response = []
    for result in results:
        response.append({
            "player": result[0],
            "team": result[1],
            "percentShotsMade": result[2],
            "nMatches": result[3],
            "nWins": result[4],
            "percentWins": result[5]
        })
    return json.dumps(response)

# PORCENTAGEM DE CADA TIPO DE ARREMESSO DIVIDIDOS EM QUARTILES

def getPlayerShotPercentage(courtArea, player):
    playerShotPercentageFromDatabase = db.engine.execute(f"""
        SELECT {courtArea}
        FROM players_shooting
        WHERE player = '{player}'
    """)
    for shotPercentage in playerShotPercentageFromDatabase:
        playerShotPercentage = shotPercentage[0]
    return playerShotPercentage


def getPercentiles(courtArea, player):
    percentagesFromTheDatabase = db.engine.execute(f"""
        SELECT {courtArea}
        FROM players_shooting
    """)
    allPlayersPercentage = []
    for percentage in percentagesFromTheDatabase:
        allPlayersPercentage.append(percentage[0])
    percentiles = []
    percentiles.append(round(np.percentile(allPlayersPercentage, 10), 2))
    percentiles.append(round(np.percentile(allPlayersPercentage, 20), 2))
    percentiles.append(round(np.percentile(allPlayersPercentage, 30), 2))
    percentiles.append(round(np.percentile(allPlayersPercentage, 40), 2))
    percentiles.append(round(np.percentile(allPlayersPercentage, 50), 2))
    percentiles.append(round(np.percentile(allPlayersPercentage, 60), 2))
    percentiles.append(round(np.percentile(allPlayersPercentage, 70), 2))
    percentiles.append(round(np.percentile(allPlayersPercentage, 80), 2))
    percentiles.append(round(np.percentile(allPlayersPercentage, 90), 2))
    percentiles.append(round(np.percentile(allPlayersPercentage, 100), 2))
    return percentiles


def getHeatmapIntensity(playerShotPercentage, percentiles):
    heatmapIntensity = -1
    if (playerShotPercentage >= percentiles[9]):
        heatmapIntensity = 8.3
    elif (playerShotPercentage >= percentiles[8]):
        heatmapIntensity = 7.50
    elif (playerShotPercentage >= percentiles[7]):
        heatmapIntensity = 6.7
    elif (playerShotPercentage >= percentiles[6]):
        heatmapIntensity = 5.8 
    elif (playerShotPercentage >= percentiles[5]):
        heatmapIntensity = 5.0
    elif (playerShotPercentage >= percentiles[4]):
        heatmapIntensity = 4.2 
    elif (playerShotPercentage >= percentiles[3]):
        heatmapIntensity = 3.3
    elif (playerShotPercentage >= percentiles[2]):
        heatmapIntensity = 2.5
    elif (playerShotPercentage >= percentiles[1]):
        heatmapIntensity = 1.7
    elif (playerShotPercentage >= percentiles[0]):
        heatmapIntensity = 0.8
    else:
        heatmapIntensity = 0
    return heatmapIntensity

@bp.route('/shotPercentage', methods=['GET'])
def getShotPercentageAndQuartilesPerCourtArea():
    args = request.args
    courtArea = args['courtArea']
    player = args['player']
    playerShotPercentage = getPlayerShotPercentage(courtArea, player)
    percentiles = getPercentiles(courtArea, player)
    heatmapIntensity = getHeatmapIntensity(playerShotPercentage, percentiles)
    return json.dumps({
        "player": player,
        "shotPercentage": playerShotPercentage,
        "heatmapIntensity": heatmapIntensity,
        "percentiles": percentiles
    })

# TIMES COM MELHOR DEFESA

@bp.route('/teamsBestDefense', methods=['GET'])
def get_teams_best_defence():
    results = db.engine.execute(f"""
        SELECT team1.team, SUM(opposing_team.fga - opposing_team.fgm) AS fieldGoalsNotTaken
        FROM team_matches team1
        JOIN team_matches opposing_team
        ON SUBSTRING(opposing_team.match_id ,LENGTH(opposing_team.match_id)-16 , LENGTH(opposing_team.match_id)) = CONCAT(team1.team ,\' in \',SUBSTRING(team1.match_id ,LENGTH(team1.match_id)-9 , LENGTH(team1.match_id))) 
        GROUP BY team1.team
        ORDER BY fieldGoalsNotTaken DESC
    """)
    response = []
    for result in results:
        response.append({
            "team1.team": result[0],
            "fieldGoalsNotTaken": result[1]
        })
    return json.dumps(response)

# Nº DE VITÓRIAS DO TIME

@bp.route('/teamWins', methods=['GET'])
def get_team_wins():
    args = request.args
    team = args['team']
    results = db.engine.execute(f"""
        SELECT team, COUNT(case when won then 1 else null end) AS totalWins
        FROM team_matches
        WHERE team = '{team}'
        GROUP BY team
    """)
    response = []
    for result in results:
        response.append({
            "team": result[0],
            "totalWins": result[1] 
        })
    return json.dumps(response)

# Nº DE PONTOS QUE O TIME FEZ NA TEMPORADA

@bp.route('/teamPointsScored', methods=['GET'])
def get_team_points_scored():
    args = request.args
    team = args['team']
    results = db.engine.execute(f"""
        SELECT team, SUM(points) AS totalPoints
        FROM team_matches
        WHERE team = '{team}'
        GROUP BY team
    """)
    response = []
    for result in results:
        response.append({
            "team": result[0],
            "totalPointsScored": result[1] 
        })
    return json.dumps(response)

# Nº DE PONTOS QUE O TIME LEVOU NA TEMPORADA

@bp.route('/teamPointsTaken', methods=['GET'])
def get_team_points_taken():
    args = request.args
    team = args['team']
    results = db.engine.execute(f"""
        SELECT '{team}' as team, CAST(SUM(subquery.pointsTaken) AS INTEGER) AS totalPointsTaken
        FROM (
            SELECT team, SUM(points) AS pointsTaken
            FROM team_matches
            WHERE match_id LIKE '%%vs. {team}%%' OR match_id LIKE '%%@ {team}%%'
            GROUP BY team
        ) subquery
    """)
    response = []
    for result in results:
        response.append({
            "team": result[0],
            "totalPointsTaken": result[1] 
        })
    return json.dumps(response)

# Nº DE PONTOS QUE O TIME FEZ E LEVOU POR JOGO

@bp.route('/teamPointsMadeAndTakenPerGame', methods=['GET'])
def get_team_points_made_and_taken_per_game():
    args = request.args
    team = args['team']
    results = db.engine.execute(f"""
        SELECT pointsScored.points, pointsTaken.points 
        FROM (
            SELECT match_id, points
            FROM team_matches
            WHERE team = '{team}'
        ) AS pointsScored
        JOIN (
            SELECT match_id, points
            FROM team_matches
            WHERE (match_id LIKE '%%vs. {team}%%' OR match_id LIKE '%%@ {team}%%')
        ) AS pointsTaken
        ON RIGHT(pointsScored.match_id, 10) = RIGHT(pointsTaken.match_id, 10)
        WHERE pointsScored.match_id LIKE '%%{team}%%' AND pointsTaken.match_id LIKE '%%{team}%%'
    """)
    response = []
    for result in results:
        response.append({
            "pointsMade": result[0],
            "pointsTaken": result[1] 
        })
    return json.dumps(response)

# Nº DE VITÓRIAS E DERROTAS DO TIME

@bp.route('/teamsWinsLosses', methods=['GET'])
def get_teams_wins_losses():
    results = db.engine.execute(f"""
        SELECT team, COUNT(case when won then 1 else null end) AS totalWins, COUNT(case when NOT won then 1 else null end) AS totalLosses
        FROM team_matches
        GROUP BY team
        ORDER BY totalWins DESC
    """)
    response = []
    for result in results:
        response.append({
            "team": result[0],
            "totalWins": result[1],
            "totalLosses": result[2] 
        })
    return json.dumps(response)

# TIMES E ACERTOS/ERROS EM CADA TIPO DE ARREMESSO

@bp.route('/teamShotsMadeAndMissed', methods=['GET'])
def get_team_shots_made_and_missed():
    args = request.args
    team = args['team']
    results = db.engine.execute(f"""
        SELECT team, SUM(ftm) AS freeThrowsMade, SUM(fta-ftm) AS freeThrowsMissed, SUM(tpm) AS threePointsMade, SUM(tpa-tpm) AS threePointsMissed, SUM(fgm-tpm) AS fieldGoalsMade, SUM((fga-fgm)-(tpa-tpm)) AS fieldGoalsMissed
        FROM team_matches
        WHERE team = '{team}'
        GROUP BY team
        ORDER BY team
    """)
    response = []
    for result in results:
        return json.dumps({
            "team": result[0],
            "freeThrowsPercentage": round((result[1] / (result[1] + result[2])) * 100, 2),
            "twoPointsPercentage":  round((result[5] / (result[5] + result[6])) * 100, 2),
            "threePointsPercentage":  round((result[3] / (result[3] + result[4])) * 100, 2),
            "totalPercentage": round(((result[1] + result[3] + result[5]) / (result[1] + result[2] + result[3] + result[4] + result[5] + result[6])) * 100, 2)
        })