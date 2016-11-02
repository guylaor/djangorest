# DJANGO REST

A simple rest service to redirect to shorten urls

## SETUP

This is using Python3, so make sure when you create the virtualenv you use python3.

~ virtualenv -p python3 venv  

then run:

~ pip install -r requirments.txt

After that, set up the database:

~ python manage.py migrate

To run tests:

~ python manage.py test

to run the project

~ python manage.py runserver

this link will show the list of all urls, and also a simple form to add a url:

http://localhost:8000/api/urls/
