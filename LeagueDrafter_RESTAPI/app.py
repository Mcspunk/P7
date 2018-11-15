import psycopg2 as psycopg2
from flask import Flask
import initial_win_pred
import json
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/nn')
def test():
    return str(initial_win_pred.predictTeamComp([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))

def fetch_champions():
    """ query data from the vendors table """
    conn = None
    try:
        conn = psycopg2.connect(host="sw703db.cgukp5oibqte.eu-central-1.rds.amazonaws.com",database="SW703DB", user="sw703", password="sw703aoe")
        cur = conn.cursor()
        cur.execute("SELECT * FROM champions ORDER BY name")
        rows = cur.fetchall()
        collection = []
        imagePaths = []
        for row in rows:
            collection.append(dict({'name' : row[0], 'orgId':row[1],'newId':row[2],'tags':row[3],'imgPath':row[4]}))
        cur.close()
        return json.dumps(collection)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


champions = fetch_champions()

@app.route('/api/get/champions')
def get_champions():
    return champions



if __name__ == '__main__':
    app.run()

