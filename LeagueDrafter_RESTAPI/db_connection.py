import psycopg2 as psy
import pickle

host = "sw703db.cgukp5oibqte.eu-central-1.rds.amazonaws.com"
database = "SW703DB"
user = "sw703"
password = "sw703aoe"

def retrieveWins():
    conn = psy.connect(host=host, database=database, user=user, password=password)
    cursor = conn.cursor()
    Wins = []
    cursor.execute('SELECT win FROM playerstats ps JOIN player p ON ps.playerstatsid = p.playerstatsid WHERE playerid % 10 = 0 ORDER BY playerid ASC LIMIT 100')
    row = cursor.fetchone()
    while row is not None:
        Wins.append(row)
        row = cursor.fetchone()
    cursor.close()
    conn.close()
    return

def retrieveDataset():
    amountOfChamps = 141
    conn = psy.connect(host=host, database=database, user=user, password=password)
    cursor = conn.cursor()
    playedChampions = []
    intermediateList = []
    cursor.execute('SELECT p.corrected_id, damage, toughness, control, mobility, utility, difficulty FROM player p JOIN  champions ch ON p.corrected_id = ch.corrected_id ORDER BY playerid ASC')
    row = cursor.fetchone()
    i=1
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
    root = cursor.execute('SELECT tree FROM pickled_tree WHERE id =%s ',id)
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

def saveTree(tree, id):
    conn = psy.connect(host=host, database=database, user=user, password=password)
    cursor = conn.cursor()
    pickledTreeId = id
    pickledTree = pickle.dumps(tree, -1)
    cursor.execute('INSERT INTO pickled_tree(id, tree) VALUES(%s, %s) ON CONFLICT(id) DO UPDATE SET tree = %s',(pickledTreeId, pickledTree, pickledTree))
    conn.commit()
    cursor.close()
    conn.close()
