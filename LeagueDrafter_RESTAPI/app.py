import datetime
import time
import uuid
import threading

import jwt
from random import *
import psycopg2 as psycopg2
from flask import Flask, make_response
import json
from flask_cors import CORS
from flask import request
import flask.sessions
import MCTS as MCTS
import db_connection as db
import initial_win_pred as nn

app = Flask(__name__)
cors = CORS(app,supports_credentials=True, resources={r"/api/*": {"origins": "*","supports_credentials":True}})
app.secret_key = "b\"\\xa7'\\x19\\xde\\x91_\\x1b\\xe0L'\\xd2\\xc0O\\xae\\x12\\xfe"
app.permanent_session_lifetime = datetime.timedelta(minutes=5)

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print("Starting " + self.name)
        clearDb(self.name,self.counter)
        print("Exiting " + self.name)

def clearDb(threadName,delay):
    while True:
        time.sleep(delay)
        print("Cleaning DB Trees")
        tree_data = db.retrieve_tress()
        print("Number of current session:",len(tree_data))
        for payload in tree_data:
            expTime = datetime.datetime.utcfromtimestamp(payload[1])
            if  expTime < datetime.datetime.utcnow():
                db.deleteTree(payload[0])
                print(payload[0],"was deleted - Expired at:",expTime)



thread1 = myThread(1,"Thread-1",60)
thread1.start()

@app.route('/api/post/endresult/',methods=['POST'])
def calculate_end_result():
    json_data = request.get_json(force=True)
    feature_vec = []
    for champion in json_data['ally_team']:
        feature_vec.append(champion)
    for champion in json_data['enemy_team']:
        feature_vec.append(champion)
    return str(nn.predictTeamComp(feature_vec)*100)


@app.route('/api/get/checksession/',methods=['GET'])
def session_check():
    sess_cookie = request.cookies.get("session")
    resp = make_response()
    resp.headers['Access-Control-Allow-Credentials'] = 'true'
    resp.headers['Access-Control-Allow-Origin'] = "http://frontend.leaguedraft.gg"

    try:
        payload = jwt.decode(sess_cookie,app.secret_key)
        return resp,200
    except jwt.ExpiredSignatureError:
        return resp,204
    except jwt.InvalidTokenError:
        return resp,204

@app.route('/api/post/newsession/',methods=['POST'])
def create_session():
    payload = {
        'exp': datetime.datetime.utcnow() + app.permanent_session_lifetime,
        'iat': datetime.datetime.utcnow(),
        'sub': str(uuid.uuid4())
    }
    resp = make_response()
    resp.headers['Access-Control-Allow-Origin'] = "http://frontend.leaguedraft.gg"
    resp.headers['Access-Control-Allow-Credentials'] = 'true'
    resp.set_cookie("session", jwt.encode(payload,app.secret_key,algorithm="HS256"),expires=payload['exp'],domain='.leaguedraft.gg')
    return resp

@app.route('/')
def hello_world():
    return 'Hello World!'

def fetch_champions():
    conn = None
    try:
        conn = psycopg2.connect(host="sw703db.cgukp5oibqte.eu-central-1.rds.amazonaws.com",database="SW703DB", user="sw703", password="sw703aoe")
        cur = conn.cursor()
        cur.execute("SELECT * FROM champions ORDER BY name")
        rows = cur.fetchall()
        collection = []
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

@app.route('/api/get/champions/',methods=['GET'])
def get_champions():
    return champions

@app.route('/api/post/currentState/',methods=['POST'])
def post_currentState():
    json_data = request.get_json(force=True)
    payload = jwt.decode(request.cookies.get("session"), app.secret_key)
    session_id = payload['sub']
    suggestions = MCTS.post_draft_turn(json_data,session_id,payload['exp'])
    return suggestions


if __name__ == '__main__':
    app.run(host='127.0.0.1', port="5000")

