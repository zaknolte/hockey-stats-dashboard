#!/bin/bash
cd backend
python manage.py makemigrations
python manage.py migrate
echo Loading data for teams...
python manage.py loaddata teams.json
echo Loading data for seasons...
python manage.py loaddata seasons.json
echo Loading data for player positions...
python manage.py loaddata playerpositions.json
echo Loading data for player stats...
python manage.py loaddata playerstats.json
echo Loading data for player seasons...
python manage.py loaddata playerseasons.json
echo Loading data for goalie seasons...
python manage.py loaddata goalieseasons.json
echo Loading data for team seasons...
python manage.py loaddata teamseasons.json