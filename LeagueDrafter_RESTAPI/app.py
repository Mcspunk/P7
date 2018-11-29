import datetime
import uuid
import psycopg2 as psycopg2
from flask import Flask
import json
from flask_cors import CORS
from flask import request
import flask.sessions

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
session = flask.session
app.secret_key = "b\"\\xa7'\\x19\\xde\\x91_\\x1b\\xe0L'\\xd2\\xc0O\\xae\\x12\\xfe"
app.config['SESSION_TYPE'] = 'filesystem'


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(minutes=10)
    session.modified = True

@app.route('/api/checksession/')
def session_check():
    if 'uid' in session:
        return flask.Response(status=200)
    else: return flask.Response(status=204)

@app.route('/api/newsession/')
def create_session():
    session['uid'] = str(uuid.uuid4())
    return flask.Response(status=200)

@app.route('/')
def hello_world():
    return 'Hello World!'

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

@app.route('/api/post/currentState',methods=['POST'])
def post_currentState():
    json_data = request.get_json(force=True)
    return json.dumps(json_data)


if __name__ == '__main__':
    app.run()

