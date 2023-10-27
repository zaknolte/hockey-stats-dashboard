#!/bin/bash
cd backend
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata teams.json
python manage.py loaddata seasons.json
python manage.py loaddata playerpositions.json
python manage.py loaddata playerstats.json
python manage.py loaddata playerseasons.json
python manage.py loaddata goalieseasons.json
python manage.py loaddata teamseasons.json