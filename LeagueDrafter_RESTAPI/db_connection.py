import psycopg2 as psy
import pickle

host = "restoreddb.cgukp5oibqte.eu-central-1.rds.amazonaws.com"
database = "SW703DB"
user = "sw703"
password = "sw703aoe"

# SELECT corrected_id FROM player ORDER BY playerid ASC LIMIT 10
# SELECT * FROM bans WHERE match.banid == bans.banid
#SELECT banid FROM match WHERE players.playersid == $s AND match.banid == bans.banid
#SELECT player.id FROM player


def get_matches(number_of_matches):
    team1 = []
    team2 = []
    match_list= []
    rows_to_collect = number_of_matches*10
    conn = psy.connect(host=host, database=database, user=user, password=password)
    cursor = conn.cursor()
    cursor2 = conn.cursor()
    cursor.execute('SELECT corrected_id FROM player ORDER BY playerid ASC LIMIT %s',[rows_to_collect])
    cursor2.execute('SELECT ban1,ban2, ban3, ban4, ban5,ban6,ban7,ban8,ban9,ban10 FROM bans ORDER BY banid ASC LIMIT %s',[number_of_matches])
    row = cursor.fetchone()
    ban_row = cursor2.fetchone()
    count = 0
    while row is not None or ban_row is not None:
        if count < 5:
            team1.append(row[0])
            count += 1
            row = cursor.fetchone()
        elif count == 10:
            count = 0
            match_list.append((team1, team2, ban_row))
            team1 = []
            team2 = []
            ban_row = cursor2.fetchone()
        else:
            team2.append(row[0])
            count += 1
            row = cursor.fetchone()

    return match_list


def retrieveDataset():
    amountOfChamps = 141
    conn = psy.connect(host=host, database=database, user=user, password=password)
    cursor = conn.cursor()
    playedChampions = []
    intermediateList = []
    cursor.execute('SELECT p.corrected_id, damage, toughness, control, mobility, utility, difficulty FROM player p JOIN  champions ch ON p.corrected_id = ch.corrected_id ORDER BY playerid ASC')
    row = cursor.fetchone()
    i = 1
    while row is not None:
        intermediateList.append(row)
        row = cursor.fetchone()
        if i % 10 == 0 and i != 0:
            playedChampions.append(intermediateList)
            intermediateList = []
        i += 1
    redTeam = []
    blueTeam = []
    for x in playedChampions:
        redTeam.append(x[0:5])
        blueTeam.append(x[5:10])
    dataset = []
    datasetrow = []
    #datasetrow = [0] * amountOfChamps
    while len(redTeam) != 0:
        for champ in redTeam[0]:
            temp = []
            temp.append(1)
            temp.extend(champ)
            datasetrow.append(temp)
        for champ in blueTeam[0]:
            temp = []
            temp.append(-1)
            temp.extend(champ)
            datasetrow.append(temp)
        dataset.append(datasetrow)
        redTeam.pop(0)
        blueTeam.pop(0)
        datasetrow = [] #[0] * amountOfChamps
    Wins = []
    cursor.execute(
        'SELECT win FROM playerstats ps JOIN player p ON ps.playerstatsid = p.playerstatsid WHERE playerid % 10 = 0 ORDER BY playerid ASC')
    row = cursor.fetchone()
    while row is not None:
        if row[0] == True:
            #Wins.append([1])
            #Wins.append([1, 0])
            Wins.append([[1, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]])
        else:
            #Wins.append([0])
            #Wins.append([0, 1])
            Wins.append([[0, 1], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]])
        row = cursor.fetchone()
    cursor.execute('SELECT corrected_id, damage, toughness, control, mobility, utility, difficulty FROM champions')
    championrow = cursor.fetchone()
    champions = []
    while championrow is not None:
        champions.append(championrow)
        championrow = cursor.fetchone()
    cursor.close()
    conn.close()
    return dataset, Wins, champions


def loadTree(session_id):
    id = session_id
    conn = psy.connect(host=host, database=database, user=user, password=password)
    cursor = conn.cursor()
    root = cursor.execute('SELECT tree FROM pickled_tree WHERE id = \'{0}\''.format(id))
    return root


def insert_winpercents():
    conn = psy.connect(host=host, database=database, user=user, password=password)
    cursor = conn.cursor()
    for champion_id in range(0,141):
        cursor.execute('SELECT COUNT(*) FROM player WHERE corrected_id =%s',[champion_id])
        totalMatches = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM player p JOIN playerstats ps ON  p.playerstatsid = ps.playerstatsid'
                              ' WHERE corrected_id =%s AND ps.win = TRUE', [champion_id])
        wins = cursor.fetchone()[0]
        winPercent = (100/totalMatches)*wins
        cursor.execute('UPDATE champions SET win_pct = %s WHERE (corrected_id = %s)', (winPercent, champion_id))
        conn.commit()
    cursor.close()
    conn.close()


def retrieve_winpercent():
    conn = psy.connect(host=host, database=database, user=user, password=password)
    cursor = conn.cursor()
    champions = []
    for champion_id in range(0, 141):
        cursor.execute('SELECT win_pct FROM champions WHERE corrected_id =%s', [champion_id])
        champions.append((champion_id, cursor.fetchone()[0]))
    cursor.close()
    conn.close()
    return champions

def retrieve_tress():
    conn = psy.connect(host=host, database=database, user=user, password=password)
    cursor = conn.cursor()
    trees = []
    cursor.execute('SELECT id,exp_time FROM pickled_tree')
    tree_row = cursor.fetchone
    while tree_row is not None:
        tree_row = cursor.fetchone()
        if(tree_row != None): trees.append(tree_row)
    cursor.close()
    conn.close()
    if(trees == None): trees = []
    return trees

def saveTree(tree, id, exp_time):
    conn = psy.connect(host=host, database=database, user=user, password=password)
    cursor = conn.cursor()
    pickledTreeId = id
    pickledTree = pickle.dumps(tree, -1)
    cursor.execute('INSERT INTO pickled_tree(id, tree, exp_time) VALUES(%s, %s, %s) ON CONFLICT(id) DO UPDATE SET tree = %s',(pickledTreeId, pickledTree,exp_time, pickledTree))
    conn.commit()
    cursor.close()
    conn.close()

def deleteTree(id):
    conn = psy.connect(host=host, database=database, user=user, password=password)
    cursor = conn.cursor()
    pickledTreeId = id
    cursor.execute('DELETE FROM pickled_tree WHERE id = \'{0}\''.format(pickledTreeId))
    conn.commit()
    cursor.close()
    conn.close()