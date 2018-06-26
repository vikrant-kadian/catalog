from flask import Flask, jsonify, request, url_for
from flask import abort, render_template, flash, redirect
from database_setup import Base, User, Manufacturer, Car
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from sqlalchemy import create_engine, desc
from flask_httpauth import HTTPBasicAuth
from functools import wraps
from flask import session as login_session
from flask import make_response

import random
import string
import requests
import httplib2
import json

app = Flask(__name__)
auth = HTTPBasicAuth()
engine = create_engine('postgresql://grader:grader@localhost/catalog')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Read Google client_secrets.json and fetch client_id
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']


# shows index/landing page
@app.route('/')
@app.route('/index/')
def welcomeHome():
    manufacturers = session.query(Manufacturer).all()
    latestCars = session.query(Car).order_by(desc(Car.id)).limit(10)
    return render_template(
        'index.html', manufacturers=manufacturers, latestCars=latestCars)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' in login_session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('logIn', next=request.url))
    return decorated_function


# shows the home page after the user log in
# user can only visit this page after log in
@app.route('/home/')
@login_required
def loggedIn():
    manufacturers = session.query(Manufacturer).all()
    latestCars = session.query(Car).order_by(desc(Car.id)).limit(10)
    return render_template(
        'home.html', manufacturers=manufacturers, latestCars=latestCars)


# shows the login page where user can log in with the google account
@app.route('/login/')
def logIn():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    if session.query(User).filter_by(email=data['email']).first():
        pass
    else:
        newUser = User(username=data['name'], email=data['email'])
        session.add(newUser)
        session.commit()
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += '''  "style = "width: 300px; height: 300px;border-radius:
        150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '''
    flash("you are now logged in as %s" % login_session['username'])
    print("done!")
    return output


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print('Access Token is None')
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']  # noqa
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        flash("You've successfully logged out")
        return redirect(url_for('welcomeHome'))
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# adds the car to the database
@app.route('/addCar/', methods=['GET', 'POST'])
@login_required
def addCar():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['desc']
        manf = request.form['cat']
        user = session.query(User).filter_by(
            username=login_session['username']).one()
        addCar = Car(
            user_id=user.id, name=name, description=description,
            manufacturer=manf)
        session.add(addCar)
        session.commit()
        return redirect(url_for('loggedIn'))
    else:
        return render_template('addCar.html')


# shows all the cars of the selected manufacturer
@app.route('/home/<manufacturer>/viewCars/')
@login_required
def viewCars(manufacturer):
    manufacturers = session.query(Manufacturer).all()
    cars = session.query(Car).filter_by(manufacturer=manufacturer).all()
    return render_template(
        'viewCars.html', manufacturers=manufacturers, cars=cars,
        manuf=manufacturer)


# shows all the cars of the selected manufacturer
# for guest users only
@app.route('/index/<manufacturer>/viewCars/')
def viewPublicCars(manufacturer):
    manufacturers = session.query(Manufacturer).all()
    cars = session.query(Car).filter_by(manufacturer=manufacturer).all()
    return render_template(
        'public_cars.html', manufacturers=manufacturers, cars=cars,
        manuf=manufacturer)


# shows the details of the selected car
# for logged in users provided with the functionality of add, edit and delete
@app.route('/home/<manufacturer>/<car>/')
@login_required
def viewCar(manufacturer, car):
    if session.query(Car).filter_by(name=car).one():
        manufacturers = session.query(Manufacturer).all()
        carDetails = session.query(Car).filter_by(name=car).one()
        return render_template(
            'car.html', carD=carDetails, manufacturers=manufacturers)
    else:
        return "Sorry car is not available ..."


# shows the details of the selected car
# for non-logged in users provided with the read only functionality
@app.route('/index/<manufacturer>/<car>/')
def viewPublicCar(manufacturer, car):
    if session.query(Car).filter_by(name=car).one():
        manufacturers = session.query(Manufacturer).all()
        carDetails = session.query(Car).filter_by(name=car).one()
        return render_template(
            'public_car.html', carD=carDetails, manufacturers=manufacturers)
    else:
        return "Sorry car is not available ..."


# edit the car details
@app.route('/<manufacturer>/<car>/edit', methods=['GET', 'POST'])
@login_required
def editCar(manufacturer, car):
    car = session.query(Car).filter_by(name=car).one()
    user = session.query(User).filter_by(email=login_session['email']).one()
    if car.user_id == user.id:
        if request.method == 'POST':
            name = request.form['name']
            description = request.form['desc']
            manuf = request.form['cat']
            car.name = name
            car.description = description
            car.manufacturer = manuf
            session.add(car)
            session.commit()
            return redirect(url_for('viewCar', manufacturer=manuf, car=name))
        else:
            return render_template('editCar.html', model=car)
    else:
        return '''<h1>Sorry %s you are not authorised to edit the details of this car.
        </h1><h2>Note: You can only perform this action on the cars you have
        added.</h2>''' % login_session['username']


# delete car from the database
@app.route('/<manufacturer>/<car>/delete', methods=['GET', 'POST'])
@login_required
def deleteCar(manufacturer, car):
    manufacturers = session.query(Manufacturer).all()
    car = session.query(Car).filter_by(name=car).one()
    user = session.query(User).filter_by(email=login_session['email']).one()
    if car.user_id == user.id:
        if request.method == 'POST':
            session.delete(car)
            session.commit()
            return redirect(url_for('viewCars', manufacturer=manufacturer))
        else:
            return render_template(
                'deleteCar.html', carD=car, manufacturers=manufacturers)
    else:
        return '''<h1>Sorry %s you are not authorised to remove this car.
        </h1><h2>Note: You can only perform this action on the cars you have
        added.</h2>''' % login_session['username']


# API endpoints for all users
@app.route('/users/json')
@login_required
def user_details():
    users = session.query(User).all()
    return jsonify(User=[u.serialize for u in users])


# API endpoints for all manufacturers and cars.
@app.route('/catalog/json')
@login_required
def catalog_information():
    manufacturers = session.query(Manufacturer).all()
    cars = session.query(Car).all()
    return jsonify(
        manufacturers=[c.serialize for c in manufacturers],
        Cars=[i.serialize for i in cars])


# API endpoints for all manufacturers.
@app.route('/manufacturers/json')
@login_required
def manufacturers_details():
    manufacturers = session.query(Manufacturer).all()
    return jsonify(manufacturers=[c.serialize for c in manufacturers])


# API endpoints for all cars of a specific manufacturer.
@app.route('/<manufacturer>/cars/json')
@login_required
def cars_information(manufacturer):
    manufacturer = session.query(Manufacturer).filter_by(
        name=manufacturer).one()
    cars = session.query(Car).filter_by(manufacturer=manufacturer).all()
    return jsonify(Items=[i.serialize for i in cars])

if __name__ == '__main__':
    print("Project is up and running")
    app.secret_key = 'secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
