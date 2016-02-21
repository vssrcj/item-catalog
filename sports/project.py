from flask import Flask, render_template, request, url_for, redirect, jsonify, flash

from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Sport, Player

# storing images
import os

from werkzeug import secure_filename

# state variable
import random
import string
from flask import session as login_session

# autherisation
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

from flask import request
from werkzeug.contrib.atom import AtomFeed
import time


app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']

engine = create_engine('sqlite:///sports.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/newPlayer/<sport_id>/', methods=['GET', 'POST'])
def newPlayer(sport_id):
    if request.method == 'POST':
        file = request.files['photo']
        if file:
            photo = file.filename
            file.save(os.path.join('static/img/', photo))
        else:
            photo = None

        player = Player(name=request.form['name'], 
                        dob=datetime.strptime(request.form['dob'], 
                        '%Y-%m-%d').date(), photo=photo,
                        sport_id=sport_id)
        session.add(player)
        session.commit()
        return redirect(url_for('sports', sport_id=sport_id))
    else:
        sport = session.query(Sport).filter_by(id=sport_id).one()
        return render_template('newPlayer.html', sport=sport, sport_id=sport_id)


@app.route('/sports/<sport_id>/')
@app.route('/sports/')
def sports(sport_id=1):
	state = ''.join(
		random.choice(string.ascii_uppercase + string.digits) for x in range(32))
	login_session['state'] = state

	if 'username' in login_session:
		profile_picture = login_session['picture']		
		admin = True
	else:
		profile_picture = None
		admin = False

	sports = session.query(Sport).all()
	players = session.query(Player).filter_by(sport_id=sport_id).all()
	return render_template('sports.html', sport_id=sport_id, sports=sports, players=players,
     					   STATE=state, profile_picture=profile_picture, admin=admin)


@app.route('/updatePlayer/<player_id>/', methods=['GET', 'POST'])
def updatePlayer(player_id):
	if 'username' not in login_session:
		return redirect(url_for('sports'))

	player = session.query(Player).filter_by(id=player_id).one()

	if request.method == 'POST':
		print 'valid'
		file = request.files['photo']
		print 'valid2'
		if file:            
			player.photo = photo = file.filename
			file.save(os.path.join('static/img/', photo))
		if request.form['name']:
			player.name = request.form['name']
		if request.form['dob']:
			player.dob = datetime.strptime(request.form['dob'], '%Y-%m-%d').date()
		session.add(player)
		session.commit()

		return redirect(url_for('sports', sport_id=player.sport_id))
	else:
		profile_picture = login_session['picture']
		return render_template('updatePlayer.html', player=player, sport_id=player.sport_id,
        						profile_picture=profile_picture)


@app.route('/deletePlayer/<player_id>/', methods=['GET', 'POST'])
def deletePlayer(player_id):
	if 'username' not in login_session:
		return redirect(url_for('sports'))

	player = session.query(Player).filter_by(id=player_id).one()
	if request.method == 'POST':
		session.delete(player)
		session.commit()
		return redirect(url_for('sports', sport_id=player.sport_id))
	else:
		profile_picture = login_session['picture']
		return render_template(
			'deletePlayer.html', player=player, profile_picture=profile_picture, sport_id=player.sport_id)


@app.route('/player/<player_id>/')
def player(player_id):
	if 'username' in login_session:
		profile_picture = login_session['picture']
		admin = True
	else:
		profile_picture = None
		admin = False

	player = session.query(Player).filter_by(id=player_id).one()
	sport = session.query(Sport).filter_by(id=player.sport_id).one()
	return render_template('player.html', player=player, sport=sport, admin=admin, profile_picture=profile_picture, sport_id=sport.id)


@app.route('/json/')
def json():
	sports = session.query(Sport).all()
	results = {}
	results["sports"] = []
	for sport in sports:	
		players = session.query(Player).filter_by(sport_id=sport.id).all()
		line = []
		for player in players:
			line.append({ "name": player.name, "dob": str(player.dob) })
		results["sports"].append({"name": sport.name, "players": line})
	
	return jsonify(results)

@app.route('/atom')
def atom():
    feed = AtomFeed('SA Sports',
                    feed_url=request.url, url=request.url_root)
    players = session.query(Player).all()
    for player in players:
        feed.add(player.name, "Sport: " + player.sport.name,
                 content_type='html',
                 author='CJ',
                 url=url_for('player', player_id=player.id),
                 updated=datetime.now())
    return feed.get_response()


@app.route('/gconnect', methods=['POST'])
def gconnect():
	# Validate state token
	if request.args.get('state') != login_session['state']:
		response = make_response(json.dumps('Invalid state paramter.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	# Obtain authorization code	
	request.get_data()
	code = request.data.decode('utf-8')
	print 'fine1'

	try:
		# Upgrade the authorization code into a credentials object
		oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
		oauth_flow.redirect_uri = 'postmessage'
		credentials = oauth_flow.step2_exchange(code)
	except FlowExchangeError:
		response = make_response(json.dumps('Failed to upgrade the authorization code.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	print 'fine2'
    # Check that the access token is valid.
	access_token = credentials.access_token
	url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
    # Submit request, parse response
	h = httplib2.Http()
	response = h.request(url, 'GET')[1]
	str_response = response.decode('utf-8')
	result = json.loads(str_response)
	print 'fine3'
    # If there was an error in the access token info, abort.
	if result.get('error') is not None:
		response = make_response(json.dumps(result.get('error')), 500)
		response.headers['Content-Type'] = 'application/json'
		return response
	print 'fine4'
    # Verify that the access token is used for the intended user.
	gplus_id = credentials.id_token['sub']
	if result['user_id'] != gplus_id:
		response = make_response(
		json.dumps("Token's user ID doesn't match given user ID."), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	print 'fine5'
    # Verify that the access token is valid for this app.
	if result['issued_to'] != CLIENT_ID:
		response = make_response(
		json.dumps("Token's client ID does not match app's."), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	print 'fine6'
	stored_access_token = login_session.get('access_token')
	stored_gplus_id = login_session.get('gplus_id')
	if stored_access_token is not None and gplus_id == stored_gplus_id:
		response = make_response(json.dumps('Current user is already connected.'), 200)
		response.headers['Content-Type'] = 'application/json'
		return response
	print 'fine7'
    # Store the access token in the session for later use.
	login_session['access_token'] = access_token
	login_session['gplus_id'] = gplus_id

	# Get user info
	userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
	params = {'access_token': access_token, 'alt': 'json'}
	answer = requests.get(userinfo_url, params=params)

	data = answer.json()

	login_session['username'] = data['name']
	login_session['picture'] = data['picture']
	login_session['email'] = data['email']
	print 'fine8'
    # see if user exists, if it doesn't make a new one
  	"""  user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '"""
	return "you are now logged in as %s" % login_session['username']

@app.route('/gdisconnect/<sport_id>/')
def gdisconnect(sport_id=1):
    # Only disconnect a connected user.
	access_token = login_session.get('access_token')
	if access_token is None:
		response = make_response(
			json.dumps('Current user not connected.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
	h = httplib2.Http()
	result = h.request(url, 'GET')[0]
	print result['status']
	if result['status'] == '200':
	    # Reset the user's sesson.
		del login_session['access_token']
		del login_session['gplus_id']
		del login_session['username']
		del login_session['email']
		del login_session['picture']

	return redirect(url_for('sports', sport_id=sport_id))


if __name__ == '__main__':
	app.secret_key = 'endless_secret'
	app.debug = True
	app.run(host='0.0.0.0', port=5000)