#!/bin/sh
export FLASK_APP=./api_calls.py
#source $(pipenv --venv)/bin/activate
source ./venv/Scripts/activate
flask run -p 3000