"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

import os, datetime, random, re
from app import app, db,login_manager
from flask_login import login_user, logout_user, current_user, login_required
from flask import render_template, request, redirect, url_for,flash,jsonify, make_response,session,abort
from forms import ProfileForm,LoginForm, SearchForm
from models import UserProfile
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin
from flask import Flask, jsonify
from flask_simple_geoip import SimpleGeoIP
from flask import request
import requests
import json
import googlemaps
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
import random
import hashlib
from googlemaps import exceptions

simple_geoip = SimpleGeoIP(app)

_GEOLOCATION_BASE_URL = "https://www.googleapis.com"

###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')

##########################################################################################################################

###############################################################################################

@app.route("/newProfile", methods=["GET", "POST"])
def newProfile():
    form = ProfileForm()
    
    if request.method == 'GET':
        return render_template('signup.html', form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            first_name = form.first_name.data
            last_name = form.last_name.data
            user_name = form.user_name.data
            password = form.password.data
            gender = form.gender.data
            email = form.email.data
            role = form.role.data
            
            isAdmin = "no"
            image = form.photo.data
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            uid = generateUserId(first_name, last_name)
            
            #Remember to add an Admin Account
            newUser = UserProfile(uid=uid, isAdmin = isAdmin , first_name=first_name, last_name=last_name, user_name=user_name,
            password=password, gender=gender, email=email, role=role, image=filename)
                
            db.session.add(newUser)
            db.session.commit()
            
            if current_user.is_authenticated and current_user.isAdmin=="yes":
                active = "active"
            else:
                active = "notactive"
        
            flash("Profile Successfully Created", "success")
            return redirect(url_for("profiles"))##########  #url_for('profile', uid=user.uid) use this just in case.
        return render_template('signup.html', form=form,active=active)

###############################################################################################################

@app.route('/profile/<uid>')
@login_required
def profile(uid):
    if current_user.is_authenticated:
        user = UserProfile.query.filter_by(uid=uid).first()
        
        if current_user.isAdmin=="yes":
            active = "active"
        else:
            active = "notactive"
            
        return render_template('profile.html', user=user, active=active)
    return render_template('login.html', active=active)

##################################################################################################################################

@app.route('/profiles', methods=['GET', 'POST'])
@login_required
def profiles():
    user_list = UserProfile.query.all()
    users = [{"First Name": user.first_name, "Last Name": user.last_name, "user_id": user.uid} for user in user_list]
    
    if request.method == 'GET':
        if user_list is not None:
            return render_template("profiles.html", users=user_list)
        else:
            flash('No Users Found', 'danger')
            return redirect(url_for("home"))
            
    elif request.method == 'POST':
        if user_list is not None:
            response = make_response(jsonify({"users": users}))                                           
            response.headers['Content-Type'] = 'application/json'            
            return response
        else:
            flash('No Users Found', 'danger')
            return redirect(url_for("home"))
#################################################################################################################################################

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # if user is already logged in, just redirect them to our secure page
        # or some other page like a dashboard
        return redirect(url_for('profile', uid=current_user.uid))

    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    # Login and validate the user.
    if request.method == 'POST' and form.validate_on_submit():
        # Query our database to see if the username and password entered
        # match a user that is in the database.
        user_name = form.user_name.data
        password = form.password.data

        # user = UserProfile.query.filter_by(username=username, password=password)\
        # .first()
        # or
        user = UserProfile.query.filter_by(user_name=user_name).first()
        #app.logger.debug(user)
        if user is not None and (user.password == password):
            remember_me = False

            if 'remember_me' in request.form:
                remember_me = True

            # If the user is not blank, meaning if a user was actually found,
            # then login the user and create the user session.
            # user should be an instance of your `User` class
            login_user(user, remember=remember_me)
            
            if user.isAdmin == "yes":
                active = "active"
            else:
                active = "notactive"
                
            flash('Logged in successfully.', 'success')

            next_page = request.args.get('next')
            # app.logger.debug(next_page)
            return render_template('profile.html',active=active,user=user)

        else:
            flash('Username or Password is incorrect.', 'danger')

    flash_errors(form)
    return render_template('login.html', form=form)
    
# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
@login_manager.user_loader
def load_user(uid):
    return UserProfile.query.get(int(uid))

#########################################################################################    
@app.route("/logout")
@login_required
def logout():
    # Logout the user and end the session
    logout_user()
    flash('You have been logged out.', 'danger')
    return redirect(url_for('login'))
    
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
), 'danger')


###################################################################################################################################
#@app.route("/locate")
#def locate():
    
    #ip_request = request.args.get('https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyBpR7ifpmENecBIWXWMyZ2Xmin7FoHDaIE/v1/ip.json')
    #my_ip = ip_request.json['ip']
    #geo_request = request.get('https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyBpR7ifpmENecBIWXWMyZ2Xmin7FoHDaIE/v1/ip/geo/' +my_ip + '.json')
    #geo_data = geo_request.json
    
    #lat = geo_data['latitude']
    #lng = geo_data['longitude']




###################################################################################################################################

@app.route('/mapview')
@login_required
def mapview():
    # creating a map in the view
    
    
    #Google Maps API
    send_url = "https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyBpR7ifpmENecBIWXWMyZ2Xmin7FoHDaIE"
    geo_req = requests.post(send_url)
    geo_json = json.loads(geo_req.text)
    location = geo_json['location']
    lat = location['lat']
    lng = location['lng']
    
    #IP Stack API
    #send_url = "http://api.ipstack.com/check?access_key=eafaee99437343b33b25f8b3dda5f942"
    #geo_req = requests.post(send_url)
    #geo_json = json.loads(geo_req.text)
    #lat = geo_json['latitude']
    #lng = geo_json['longitude']
    
    mymap = Map(
        identifier="view-side",
        lat=lat,
        lng=lng,
        markers=[
          {
             'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
             'lat': lat,
             'lng': lng,
             'infobox': "<b>Hello World</b>"
          }
        ]
    )
    
    return render_template('mapview.html',mymap=mymap, lat=lat, lng=lng)
    
####################################################################################################################################
"""
@app.route('/search', methods=["GET", "POST"])
def search():
    if request.method == 'POST' and form.validate_on_submit():
        
        apiKey="AIzaSyBpR7ifpmENecBIWXWMyZ2Xmin7FoHDaIE"
        address = form.search.data
        url = ('https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}'.format(address.replace(' ','+'), apiKey))
    
    return render_template('search.html')
"""
#####################################################################################################################################



###
# The functions below should be applicable to all Flask apps.
###

def generateUserId(first_name, last_name):
    temp = re.sub('[.: -]', '', str(datetime.datetime.now()))
    temp = list(temp)
    temp.extend(list(map(ord,first_name)))
    temp.extend(list(map(ord,last_name)))
    random.shuffle(temp)
    temp = list(map(str,temp))
    return int("".join(temp[:7]))%10000000 


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
