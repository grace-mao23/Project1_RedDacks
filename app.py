# RedDacks: Nahi Khan, Grace Mao, Sophie Nichol, Jackson Zou
# SoftDev1 pd9
# P01 - ArRESTed Development
# 2019-11-21

from flask import Flask, render_template, request, redirect, url_for, session, flash
from utl.db import insert, get, setup, update_user, update_searches
from utl.auth import auth, checkAuth, register
from utl.apistuff import newsapi, pullcountries, newyorktimesapi, guardianapi, comparecountry
import urllib.request, json, sqlite3, os

app = Flask(__name__)
app.secret_key = "Dacks"

# pull from countries API
# set up database connection
setup()
countries = pullcountries()
#print(countries)

# root route
@app.route("/")
def root():
    if checkAuth(): #if you've already logged in
        return redirect(url_for('home'))
    return redirect(url_for('login'))

# login page
@app.route("/login")
def login():
    if checkAuth():
        return redirect(url_for('home'))
    return render_template('login.html')

# signup page
@app.route("/signup")
def signup():
    if checkAuth():
        return redirect(url_for('home'))
    return render_template('signup.html')

# authentication page --> checking if the login is correct
@app.route("/auth")
def authen():
    if auth(request.args['username'], request.args['password']): #authentication method imported
        session["userID"] = True
        session["currentID"] = request.args['username']
        return redirect(url_for('home'))
    if get("users", "username", "WHERE username = '%s'" % request.args['username']): #if the username exists
        return render_template('login.html', error=True, message='Password Incorrect')
    return render_template('login.html', error=True, message='Username Not Found') #username doesn't exist

# authentication of signup --> checking if the registration is valid
@app.route("/register")
def reg():
    if (request.args['password'] != request.args['password2']): #passwords entered don't match
        return render_template('signup.html', error=True, message="Passwords Don't Match")
    if (request.args['username'] == get("users", "username", "WHERE username = '%s'" % request.args['username'])): #username already in database
        return render_template('signup.html', error=True, message="Username Already Taken")
    if register(request.args['username'], request.args['password']): #successful registration
        session["userID"] = True
        return redirect(url_for("home"))

# homepage
@app.route("/home")
def home():
    # loading dog API
    url = "https://random.dog/woof.json"
    response = urllib.request.urlopen(url)
    response = response.read()
    data = json.loads(response)
    while (data['url'][-1] == '4'): # mp4s are not displayable
        response = urllib.request.urlopen(url)
        response = response.read()
        data = json.loads(response)
    return render_template('home.html', dog=data['url'])

# account settings page
@app.route("/settings")
def settings():
    return render_template('settings.html');

# request to change account settings
@app.route("/change_settings")
def changing():
    # no password stuff entered --> change Username
    if (request.args['check_password'] == ''):
        if (request.args['new_password'] != '' or request.args['confirm_password'] != ''): #if other password fields filled out, something's wrong
            return render_template('settings.html', error2=True, message="Necessary Fields Not Filled Out")
        # change Username
        if (request.args['newusername'] == ''): #if username fields not filled out, something's wrong
            return render_template('settings.html', error1=True, message="Necessary Fields Not Filled Out")
        if (request.args['newusername'] == get("users", "username", "WHERE username = '%s'" % request.args['newusername'])[0][0]): #username is in database already
            return render_template('settings.html', error1=True, message="Username Already Taken")
        update_user(session['currentID'], "username", request.args['newusername']) #updating the database imported
        return render_template('settings.html', changed1=True)
    else: # password being changed
        if (request.args['new_password'] == '' or request.args['confirm_password'] == ''): #if password fields not filled out, something's wrong
            return render_template('settings.html', error2=True, message="Necessary Fields Not Filled Out")
        if (request.args['check_password'] != get("users", "hashpassword", "WHERE username = '%s'" % session['currentID'])[0][0]): #old password not correct
            return render_template('settings.html', error2=True, message="Incorrect Password")
        if (request.args['new_password'] != request.args['confirm_password']): #passwords don't match
            return render_template('settings.html', error2=True, message="Passwords Don't Match")
        update_user(session['currentID'], "hashpassword", request.args['new_password']) #updating the database
        return render_template('settings.html', changed2=True)

# logout page
@app.route("/logout")
def logout():
    session.pop("userID")
    return redirect("/")

# search page for a country
@app.route("/search")
def search():
    #blah = get("countries", "code", "WHERE name == '%s'" % request.args['query'])[0][0]
    #print(blah)
    #return "poo"
    #session['countrycode'] = countries[request.args['query']]
    #session['country'] = request.args['query']
    country = comparecountry(request.args['query'], countries)
    if country == "BOO":
        return redirect(url_for("home"))
    #update_searches(country, userID)
    session['countrycode'] = countries[country]
    session['country'] = country
    return render_template('searchedcountry.html', country = country)

# search page for a country and category
@app.route("/search/<category>")
def fullsearch(category):
    articles = newsapi(session['countrycode'], category)
    newarticles = newyorktimesapi(session['country'], category)
    #guardian = guardianapi(session['country'], category)
    #print(guardian)
    #print(newarticles)
    return render_template('results.html',
                            category = category,
                            country = session['country'].capitalize(),
                            articles = articles,
                            newarticles = newarticles)
                            #guardian = guardian)

if __name__ == "__main__":
    app.debug = True
    app.run()
