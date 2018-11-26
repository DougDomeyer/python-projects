This is a program that allows the user to select a year of a presidential and it tells the user who the candidates were and displays the map of the
United states of America where each state changes color depending on how the state voted.
Blue for Democrats, Red for Republicans, green is independent, and yellow is no information.

The program uses beautiful soup, datamaps instructions can be found at http://datamaps.github.io/
and d3 for javascript that uses online link that might change. Run the program using Flask.

To run download Flask and in cmd use go to the application file then use set FLASK_APP=temp.py
then flask run. If votingdata.sqlite is not in templates folder run collectcandidates from the same file.
It will take a bit to collect all the data.