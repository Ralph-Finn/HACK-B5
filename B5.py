from flask import Flask
app = Flask(__name__)
from flask import request
import json
import person
from flask import render_template

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/botUI')
def botUI():
    return render_template('botUI.html')

@app.route('/getBookData')
def getBookData():
    t = person.data()
    print(t)
    return json.dumps(t['bestBook']+"==========="+t['bestBookComment'],ensure_ascii=False)

@app.route('/getMusicData')
def getMusicData():
    t = person.data()
    print(t)
    return json.dumps(t['bestMusic']+"==========="+t['bestMusicComment'],ensure_ascii=False)

@app.route('/getMovieData')
def getMovieData():
    t = person.data()
    print(t)
    return json.dumps(t['bestMovie']+"==========="+t['bestMovieComment'],ensure_ascii=False)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
