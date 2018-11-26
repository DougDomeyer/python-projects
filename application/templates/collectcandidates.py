import sqlite3
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
def candidates():
    conn = sqlite3.connect('votingdata.sqlite')
    curr = conn.cursor()
    curr2 = conn.cursor()
    curr.row_factory = sqlite3.Row
    curr.execute('select distinct year from maindata')
    url1 = 'https://en.wikipedia.org/wiki/United_States_presidential_election,_'
    ln = 0
    for row in curr:
        num = row['year']
        url = url1 + str(num)
        html = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table', attrs={'class' : 'infobox vevent' })#finds specific table in html
        #result = findrows( table)
        #candidatenames= table.find_all('tr')[5]
        parties = table.find_all('tr')[8]#get to the correct row for parties

        party1 = parties.find_all('td')[0].text#get party 1
        party2 = parties.find_all('td')[1].text#get party 2

        candidatenames1= table.find_all('tr')[7]
        name1 = candidatenames1.find_all('td')[0].text #get candidate 1
        name2 = candidatenames1.find_all('td')[1].text #get candidate 2
        if party1.strip() == 'Republican': #puts information in correct possition
            curr2.execute('''
            INSERT or REPLACE INTO candidates (year, republican, democratic) VALUES (?,?,?)''', (num,name1, name2,))
        if party2.strip() == 'Republican':
            curr2.execute('''
            INSERT or REPLACE INTO candidates (year, republican, democratic) VALUES (?,?,?)''', (num,name2, name1,))
        print(str(party1) + " = " + str(name1) + ",  " + str(party2) + " = " + str(name2))
        ln = ln + 1
        if ln % 10 == 0:
            conn.commit()
    conn.commit()
        #print(num)
        #print(str(party1) + " = " + str(name1) + ",  " + str(party2) + " = " + str(name2))

candidates()
#link = rord2.find_all('a')[0].text
#secondspot =  rord.find_all('td')[1]
#link1 = secondspot.find_all('a')[0].text
#print(table)
