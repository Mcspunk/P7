from flask import Flask
import initial_win_pred

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/nn')
def test():
    return str(initial_win_pred.predictTeamComp([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))


if __name__ == '__main__':
    app.run()
