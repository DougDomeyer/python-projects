from flask import Flask
import json
import sqlite3

app = Flask(__name__)
from flask import render_template
@app.route('/map')
def hola():
    return render_template('map.html')

@app.route('/data/<year>', methods=['GET'])
def getinfo(year = 2008):
    conn = sqlite3.connect('templates/votingdata.sqlite')
    cur = conn.cursor()
    cur.row_factory = sqlite3.Row
    cur.execute('select maindata.demvote, maindata.repvote, maindata.indwin, state.statename, state.initials from maindata, state where state.id = maindata.stateid and maindata.year = ?', (year,))
    allinf = {}
    count = 0
    for row in cur :
        allinf[count] = {}
        allinf[count]['demvote'] = row['demvote']
        allinf[count]['repvote'] = row['repvote']
        allinf[count]['indwin'] = row['indwin']
        allinf[count]['statename'] = row['statename']
        allinf[count]['initials'] = row['initials']
        count += 1

    cur.execute('select republican, democratic from candidates where year = ?', (year,))
    for row in cur:
        allinf[count] = {}
        allinf[count]['dem'] = row['democratic']
        allinf[count]['rep'] = row['republican']
    return(json.JSONEncoder().encode(allinf))

@app.route('/years/', methods=['GET'])
def getyear():
    yearnum = {}
    conn = sqlite3.connect('templates/votingdata.sqlite')
    cur = conn.cursor()
    cur.row_factory = sqlite3.Row
    cur.execute('select DISTINCT year From maindata')
    count = 0
    for row in cur:
        yearnum[count] = row['year']
        count += 1
    return(json.JSONEncoder().encode(yearnum))
@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)
