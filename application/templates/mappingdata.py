import json
import sqlite3
conn = sqlite3.connect('votingdata.sqlite')
cur = conn.cursor()
cur.row_factory = sqlite3.Row

cur.execute('select maindata.demvote, maindata.repvote, maindata.indwin, state.statename, state.initials from maindata, state where state.id = maindata.stateid and maindata.year = "2016"')
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

year = 2016
cur.execute('select republican, democratic from candidates where year = ?', (year,))
for row in cur:
    allinf[count] = {}
    allinf[count]['dem'] = row['democratic']
    print(row['democratic'])
print(allinf[count]['dem'])
#count = 0
#for row in cur :
#    print(row.keys())

#year = 2008
#cur.execute('select republican, democratic from candidates where year = ?', (year,))
#allinf[count] = {}
#for row in cur:
#    print(row.keys())
#    print(row['democratic'])
