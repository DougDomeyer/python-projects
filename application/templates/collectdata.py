import sqlite3
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup

def findrows( table): #assist function below in finding correct position for info
    rows= table.find_all('tr')[1]
    ro = table.find_all('th')
    party = 0
    percent = 0
    rownum = 0
    for row in ro:
        ro2 = row.text
        if rownum != 0:
            if ro2.strip() == 'Party':
                #print('party on line' + str(rownum))
                party = rownum
            if ro2.strip() == 'Percentage':
                #print('party on line' + str(rownum))
                percent = rownum
        rownum += 1
    return {'party': party, 'percent':percent}

def getrepublicanvotehardcodedpart(year, state): #hard coded for certain states and years as the site didn't work the same or wasn't there
    state = state.replace('"', '')
    state = state.replace(' ', '_')
    if str(year) == '1944':
        if state == 'South_Carolina':
            return {'reppercent': 4.46, 'indwin': False}
        if state == 'Tennessee':
            return {'reppercent': 39.2, 'indwin': False}
        if state == 'Rhode_Island':
            return {'reppercent': 41.26, 'indwin': False}
        if state == 'North_Carolina':
            return {'reppercent': 33.3, 'indwin': False}

    if str(year) == '1948':
        if state == 'Mississippi':
            return {'reppercent': 2.62, 'indwin': True}
        if state == "South_Carolina":
            return {'reppercent' : 3.78, 'indwin' : True}

    if str(year) == '1952':
        if state == "South_Carolina":
            return {'reppercent' : 49.3, 'indwin' : False}
    if str(year) == '1980' and state == 'Alaska':
        return {'reppercent' : 54.34, 'indwin' : False}
    if str(year) == '2016' and state == 'Montana':
        return {'reppercent' : 56.2, 'indwin' : False}

    return {'reppercent': 200.62, 'indwin': False}

def getrepublicanvote(year, state): #uses BeautifulSoup to search html of wikipedia pages to get information
    state = state.replace('"', '')
    if state == "DC":
        state = 'the District of Columbia'
    state = state.replace(' ', '_')
    url1 = 'https://en.wikipedia.org/wiki/United_States_presidential_election_in_'
    filler = ',_'
    url = url1 + str(state) + filler + str(year)#puts url together
    print (url)
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser') #reads and parses html to easily work with
    correctspot = 0
    table = soup.find('table', attrs={'class' : 'infobox vevent' })#finds specific table in html
    result = findrows( table)
    rord = table.find_all('tr')[result['party']+5]
    rord2 = rord.find_all('td')[0]
    link = rord2.find_all('a')[0].text  #gets the first link either republican, democratic or independent in table
    secondspot =  rord.find_all('td')[1]
    link1 = secondspot.find_all('a')[0].text#gets the second link in the table
    independentwin = False# mostly is false
    print(link + ' and ' + link1)
    if (link.strip() != "Republican") and (link.strip() != "Democratic"): #if the first link isn't democratic or Republican it means independent won
        independentwin = True
    if link.strip() == "Republican": #if gets the correct position of where the republican nominee is on the table
        correctspot = 0
    elif link1.strip() == "Republican":
        correctspot = 1
    else:
        correctspot = 2
    row = table.find_all('tr')[result['percent']+5]
    print(correctspot)
    spot = row.find_all('td')[correctspot].text #gets the percentage for republican nominee
    spot = spot.replace('%', '') #get rid of percent sign
    return {'reppercent': spot, 'indwin': independentwin} #returns republican percent and if an independent win

#hardcoded states and initals as they won't change and it was easier this way
def initials():
    return {'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA',
    'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME','Maryland': 'MD',
    'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi':'MS', 'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ',
    'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania' : 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
    'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY', 'DC':'DC' }




#connects to votingdata.sqlite
conn = sqlite3.connect('votingdata.sqlite')
curr = conn.cursor()
#creates all tables needed in sqlite
curr.executescript('''
DROP TABLE IF EXISTS maindata;
DROP TABLE IF EXISTS state;
DROP TABLE IF EXISTS candidates;
CREATE TABLE maindata (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    stateid INTEGER,
    demvote FLOAT,
    repvote FLOAT,
    year INTEGER,
    south Boolean,
    indwin Boolean
    );
CREATE TABLE state (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    statename TEXT UNIQUE,
    initials TEXT UNIQUE);
CREATE TABLE candidates (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    year INTEGER UNIQUE,
    republican TEXT,
    democratic TEXT);
''')

filehandler = open("presidentialElections.csv")#file that contains initial information
stateinitials = initials()
ln = 0
errors = "errors "
for line in filehandler:    #goes through each line and gets information
    if ln == 0:
        ln = ln + 1
        continue
    linesplit = line.split(",")
    if int(linesplit[3]) < 1944:    #skip the information if it is before 1944 because the most of the elections don't have a page on wikipedia
        continue
    try:
        state = linesplit[1].replace('"', '')
        if (str(linesplit[3]) == '2016') and (state == 'Montana'):  #special case that I had to check before going to the website
            voteresults = getrepublicanvotehardcodedpart(linesplit[3], linesplit[1]) #gets information that is hardcoded because this one is setup differently than the other sites
        else:
            voteresults = getrepublicanvote(linesplit[3], linesplit[1]) #gets information from site
    except:
        voteresults = getrepublicanvotehardcodedpart(linesplit[3], linesplit[1]) #if the site doesn't work it checks the hardcoded information
        errors = errors + str(linesplit[3]) + ' ' + str(linesplit[1] +", ") #string that contains all states and years that the website didn't work on

    curr.execute('''
    INSERT or IGNORE INTO state (statename, initials) VALUES (?,?)''', (state,stateinitials[state],))
    curr.execute('SELECT id FROM state WHERE statename = ? ', (state,)) #puts the state and it's initials in the state table
    state_id = curr.fetchone()[0] #get id for table and put it in maindata

    curr.execute('''INSERT OR REPLACE INTO maindata
        (stateid, demvote, repvote, year, south, indwin)
        VALUES ( ?, ?, ?, ?, ?, ?)''',
        (state_id, linesplit[2], float(voteresults['reppercent']), linesplit[3], linesplit[4], voteresults['indwin'],) )
#sql insert data needed in the main table
    ln = ln + 1
    if ln % 10 == 0: #commits after every ten times through
        conn.commit()
        print(errors)
conn.commit() #commits any extra queries
import collectcandidates as cc #runs a program that collects the names of the presidential nominees
