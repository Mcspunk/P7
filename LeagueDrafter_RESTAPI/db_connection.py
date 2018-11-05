import psycopg2 as psy
import numpy as np

class dbConnector:

    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password

    def retrieveWins(self):
        conn = psy.connect(host=self.host, database=self.database, user=self.user, password=self.password)
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

    def retrieveDataset(self):
        amountOfChamps = 141

        conn = psy.connect(host=self.host, database=self.database, user=self.user, password=self.password)
        cursor = conn.cursor()

        playedChampions = []
        intermediateList = []

        cursor.execute('SELECT corrected_id FROM player ORDER BY playerid ASC')
        row = cursor.fetchone()

        i=1
        while row is not None:
            intermediateList.extend(row)
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

        datasetrow = [0] * amountOfChamps

        while len(redTeam) != 0:

            for champ in redTeam[0]:
                datasetrow[champ] = 1
            for champ in blueTeam[0]:
                datasetrow[champ] = -1

            dataset.append(datasetrow)
            redTeam.pop(0)
            blueTeam.pop(0)
            datasetrow = [0] * amountOfChamps

        Wins = []

        cursor.execute(
            'SELECT win FROM playerstats ps JOIN player p ON ps.playerstatsid = p.playerstatsid WHERE playerid % 10 = 0 ORDER BY playerid ASC')
        row = cursor.fetchone()

        while row is not None:
            if row[0] == True:
                #Wins.append([1])
                Wins.append([1, 0])
            else:
                #Wins.append([0])
                Wins.append([0, 1])
            row = cursor.fetchone()

        cursor.close()
        conn.close()

        return dataset, Wins


