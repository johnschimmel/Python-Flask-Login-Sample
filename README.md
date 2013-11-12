# Flask Login Demo

Demo: <http://itppylogindemo.herokuapp.com/>

## Flask Login

This code sample makes use of Flask and Flask-Login, a library that manages User registration, log in, session and logout functionality. 

[Flask-Login Documentation](https://flask-login.readthedocs.org/en/latest/)

### Demo App ..
* register and login users. 
* create notes saved in database and associated to a specific user.
* users can edit their own notes.

### To get started

* Download code
* Create Git repo

		git init
		git add .
		git commit -am "init commit"

* Create a virtual environment 

		virtualenv venv

* Install all requirements for app

		. runpip

	or 

		. venv/bin/activate
		pip install -r requirements.txt

* Create Heroku app

		heroku create

* Add MongoLab Starter Addon to your app, from your code directory in Terminal

		heroku addons:add mongolab

* Add MONGOLAB_URI from Heroku config to your .env file

		heroku config --shell | grep MONGOLAB_URI >> .env

### Create a SECRET_KEY for your .env and Heroku Config

We need a SECRET_KEY for salting the user passwords.

* Open your .env and add a new line 

		SECRET_KEY=SOMETHINGSECRETANDRANDOMHERE
		DEBUG=True

* We need to add this secret key to Heroku config vars too

		heroku config:add SECRET_KEY=SOMETHINGSECRETANDRANDOMHERE

This will add a new key and value to the App on Heroku.


## Run it

With your MONGOLAB_URI and SECRET_KEY configured in .env and on Heroku config you should be good to run the code.

Run,

	. start

or 

	. venv/bin/activate
	foreman start


## The routes

* / - main page - display all notes. 
* /notes/:note_id - display an individual note
* /notes/:note_id/edit - display edit page for note, only user that created the note can edit.
* /register - create a new user
* /login - login with registered email and password
* /logout - logout user


## Flask Blueprints - Modular Flask Development

[Flask Blueprint docs](http://flask.pocoo.org/docs/blueprints/)

Blueprints allow you to separate your app into modules removing core code from App.py and making the Blueprints little apps that get registered and work together in one large application.

## Running the server

### run_server.py

	foreman start

If you don't have foreman, download and install the [Heroku Toolbelt](http://toolbelt.heroku.com)

run_server.py does the following tasks to get the app ready

* Imports app.py - app.py implements database connection, session management, login manager setup.
* Imports blueprints
	* notes.py - routes for all note display, create and edit
	* auth.py - routes for login, registration and logout


