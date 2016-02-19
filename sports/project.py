from flask import Flask, render_template, request, url_for, redirect, jsonify
from datetime import datetime
import os
from werkzeug import secure_filename

app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Sport, Player

import random
import string

from flask import session as login_session

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
        return render_template('newPlayer.html', sport=sport)


@app.route('/sports/<sport_id>/')
@app.route('/sports/')
def sports(sport_id=1):
    state = ''.join(
        random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    login_session['state'] = state

    sports = session.query(Sport).all()
    players = session.query(Player).filter_by(sport_id=sport_id).all()   
    return render_template('sports.html', sport_id=sport_id, sports=sports, players=players, STATE=state)


@app.route('/updatePlayer/<player_id>/', methods=['GET', 'POST'])
def updatePlayer(player_id):
    player = session.query(Player).filter_by(id=player_id).one()
    
    if request.method == 'POST':
        file = request.files['photo']
        if file:            
            player.photo = photo = file.filename
            file.save(os.path.join('static/img/', photo))
        if request.form['name']:
            player.name = request.form['name']
        if request.form['dob']:
            player.dob = datetime.strptime(request.form['dob'], '%Y-%m-%d').date()
        print '2'
        session.add(player)
        session.commit()
    	return redirect(url_for('sports', sport_id=player.sport_id))
    else:
        return render_template('updatePlayer.html', player=player)


@app.route('/deletePlayer/<player_id>/', methods=['GET', 'POST'])
def deletePlayer(player_id):
    player = session.query(Player).filter_by(id=player_id).one()
    if request.method == 'POST':
        session.delete(player)
        session.commit()
        return redirect(url_for('sports', sport_id=player.sport_id))
    else:
        return render_template(
            'deletePlayer.html', player=player)


@app.route('/player/<player_id>/')
def player(player_id):
    player = session.query(Player).filter_by(id=player_id).one()
    sport = session.query(Sport).filter_by(id=player.sport_id).one()
    return render_template('player.html', player=player, sport=sport)


@app.route('/sports/json/')
def sportsJson():
    sports = session.query(Sport).all()
    return jsonify(Sports=[sport.serialize for sport in sports])


# @app.route('/players/json/<sport_id>/')
# def playersJson(sport_id):
#    players = session.query(Player).filter_by(sport_id=sport_id).all()
#    return jsonify(Players=[player.serialize for player in players])


if __name__ == '__main__':
    app.secret_key = 'endless_secret'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)