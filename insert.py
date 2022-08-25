from app import db
from app.models import TeamMatches, PlayersMatches, PlayersShooting, PlayersInfo
from datetime import datetime
import sqlalchemy
import csv

def feet_and_inches_to_cm(feet, inches):
    return int(round(feet*30.48 + inches*2.54))

def lbs_to_kg(lbs):
    return int(round(lbs * 453.592 / 1000))

def insert_team_matches():
    rows = []
    with open("data/team_matches.csv", 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            match_id = row[1] + ' in ' + row[2]
            team = row[0]
            won = True if row[3] == 'W' else False
            points = int(row[4])
            fgm = int(row[5])
            fga = int(row[6])
            fgp = float(row[7])
            tpm = int(row[8])
            tpa = int(row[9])
            tpp = float(row[10])
            ftm = int(row[11])
            fta = int(row[12])
            ftp = float(row[13])
            oreb = int(row[14])
            dreb = int(row[15])
            reb = int(row[16])
            ast = int(row[17])
            stl = int(row[18])
            blk = int(row[19])
            tov = int(row[20])
            team_matches = TeamMatches(
                match_id=match_id,
                team=team,
                won=won,
                points=points,
                fgm=fgm,
                fga=fga,
                fgp=fgp,
                tpm=tpm,
                tpa=tpa,
                tpp=tpp,
                ftm=ftm,
                fta=fta,
                ftp=ftp,
                oreb=oreb,
                dreb=dreb,
                reb=reb,
                ast=ast,
                stl=stl,
                blk=blk,
                tov=tov
            )
            db.session.add(team_matches)
            db.session.commit()

def insert_players_matches():
    rows = []
    with open("data/players_matches.csv", 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        count = 1
        for row in csvreader:
            id = count
            player = row[0]
            team = row[1]
            match_id = row[2] + ' in ' + row[3]
            won = True if row[4] == 'W' else False
            points = int(row[5])
            fgm = int(row[6])
            fga = int(row[7])
            fgp = float(row[8])
            tpm = int(row[9])
            tpa = int(row[10])
            tpp = float(row[11])
            ftm = int(row[12])
            fta = int(row[13])
            ftp = float(row[14])
            oreb = int(row[15])
            dreb = int(row[16])
            reb = int(row[17])
            ast = int(row[18])
            stl = int(row[19])
            blk = int(row[20])
            tov = int(row[21])       
            players_matches = PlayersMatches(
                id=id,
                player=player,
                team=team,
                match_id=match_id,
                won=won,
                points=points,
                fgm=fgm,
                fga=fga,
                fgp=fgp,
                tpm=tpm,
                tpa=tpa,
                tpp=tpp,
                ftm=ftm,
                fta=fta,
                ftp=ftp,
                oreb=oreb,
                dreb=dreb,
                reb=reb,
                ast=ast,
                stl=stl,
                blk=blk,
                tov=tov
            )
            db.session.add(players_matches)
            db.session.commit()
            count += 1

def insert_players_shooting():
    rows = []
    with open("data/players_shooting.csv", 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            player = row[0]
            team = row[1]
            age = float(row[2])
            rar_fgm = float(row[3])
            rar_fga = float(row[4])
            rar_fgp = float(row[5])
            itp_fgm = float(row[6])
            itp_fga = float(row[7])
            itp_fgp = float(row[8])
            mrg_fgm = float(row[9])
            mrg_fga = float(row[10])
            mrg_fgp = float(row[11])
            lc3_fgm = float(row[12])
            lc3_fga = float(row[13])
            lc3_fgp = float(row[14])
            rc3_fgm = float(row[15])
            rc3_fga = float(row[16])
            rc3_fgp = float(row[17])
            cn3_fgm = float(row[18])
            cn3_fga = float(row[19])
            cn3_fgp = float(row[20])
            ab3_fgm = float(row[21])
            ab3_fga = float(row[22])
            ab3_fgp = float(row[23])      
            players_shooting = PlayersShooting(
                player=player,
                team=team,
                age=age,
                rar_fgm=rar_fgm,
                rar_fga=rar_fga,
                rar_fgp=rar_fgp,
                itp_fgm=itp_fgm,
                itp_fga=itp_fga,
                itp_fgp=itp_fgp,
                mrg_fgm=mrg_fgm,
                mrg_fga=mrg_fga,
                mrg_fgp=mrg_fgp,
                lc3_fgm=lc3_fgm,
                lc3_fga=lc3_fga,
                lc3_fgp=lc3_fgp,
                rc3_fgm=rc3_fgm,
                rc3_fga=rc3_fga,
                rc3_fgp=rc3_fgp,
                cn3_fgm=cn3_fgm,
                cn3_fga=cn3_fga,
                cn3_fgp=cn3_fgp,
                ab3_fgm=ab3_fgm,
                ab3_fga=ab3_fga,
                ab3_fgp=ab3_fgp
            )
            db.session.add(players_shooting)
            db.session.commit()


def insert_players_info():
    rows = []
    with open("data/players_info.csv", 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            try:
                player = row[0]
                team = row[1]
                height = feet_and_inches_to_cm(int(row[2][0]), int(row[2][2:]))
                weight = lbs_to_kg(int(row[3][0:4]))
                players_info = PlayersInfo(
                    player=player, 
                    team=team, 
                    height=height, 
                    weight=weight
                )
                db.session.add(players_info)
                db.session.commit()
            except sqlalchemy.exc.IntegrityError:
                print(f'Player {player} does not appear in PlayersShooting model, will be disconsidered')
                db.session.rollback()


if __name__ == '__main__':
    insert_team_matches()
    insert_players_shooting()
    insert_players_info()
    insert_players_matches()
