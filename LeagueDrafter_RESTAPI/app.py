import datetime
import uuid
import jwt
import psycopg2 as psycopg2
from flask import Flask, make_response
import json
from flask_cors import CORS
from flask import request
import flask.sessions
#import MCTS as MCTS

app = Flask(__name__)
cors = CORS(app,supports_credentials=True, resources={r"/api/*": {"origins": "*","supports_credentials":True}})
app.secret_key = "b\"\\xa7'\\x19\\xde\\x91_\\x1b\\xe0L'\\xd2\\xc0O\\xae\\x12\\xfe"
app.permanent_session_lifetime = datetime.timedelta(minutes=10)
currentSession = []


@app.route('/api/get/checksession/',methods=['GET'])
def session_check():
    sess_cookie = request.cookies.get("session")
    resp = make_response()
    resp.headers['Access-Control-Allow-Credentials'] = 'true'
    resp.headers['Access-Control-Allow-Origin'] = "http://127.0.0.2:8080"

    try:
        payload = jwt.decode(sess_cookie,app.secret_key)
        return resp,200
    except jwt.ExpiredSignatureError:
        currentSession.remove(sess_cookie)
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
    currentSession.append(payload)
    resp = make_response()
    resp.headers['Access-Control-Allow-Origin'] = "http://127.0.0.2:8080"
    resp.headers['Access-Control-Allow-Credentials'] = 'true'
    resp.set_cookie("sesh",jwt.encode(payload,app.secret_key,algorithm="HS256"),expires=payload['exp'],domain="127.0.0.2")
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


#champions = fetch_champions()

@app.route('/api/get/champions')
def get_champions():
    return flask.Response(status=200)

@app.route('/api/post/currentState',methods=['POST'])
def post_currentState():
    json_data = request.get_json(force=True)
    payload = jwt.decode(request.cookies.get("session"), app.secret_key)
    session_id = payload['sub']
    #suggestions = MCTS.post_draft_turn(json_data,session_id)
    return 0


if __name__ == '__main__':
    app.run()

