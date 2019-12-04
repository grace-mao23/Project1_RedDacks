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
    session["error"] = False
    session["message"] = ""
    session["e1"] = False
    session["e2"] = False
    #print(countries)
    if checkAuth(): #if you've already logged in
        return redirect(url_for('home'))
    return redirect(url_for('login'))

# login page
@app.route("/login")
def login():
    #print(session['userID'])
    if checkAuth():
        return redirect(url_for('home'))
    return render_template('login.html', error=session["error"], message=session['message'])

# signup page
@app.route("/signup")
def signup():
    if checkAuth():
        return redirect(url_for('home'))
    return render_template('signup.html', error=session["error"], message=session["message"])

# authentication page --> checking if the login is correct
@app.route("/auth")
def authen():
    if auth(request.args['username'], request.args['password']): #authentication method imported
        session["userID"] = True
        session["currentID"] = request.args['username']
        session["error"] = False
        return redirect(url_for('home'))
    if get("users", "username", "WHERE username = '%s'" % request.args['username']): #if the username exists
        session["error"] = True
        session["message"] = "Password Incorrect"
        return redirect(url_for('login'))
        #return render_template('login.html', error=True, message='Password Incorrect')
    session["error"] = True
    session["message"] = "Username Not Found"
    return redirect(url_for('login')) #username doesn't exist

# authentication of signup --> checking if the registration is valid
@app.route("/register")
def reg():
    if (request.args['password'] != request.args['password2']): #passwords entered don't match
        session["error"] = True
        session["message"] = "Passwords Don't Match"
        return redirect(url_for('signup'))
    if (request.args['username'] == get("users", "username", "WHERE username = '%s'" % request.args['username'])[0][0]): #username already in database
        session["error"] = True
        session["message"] = "Username Already Taken"
        return redirect(url_for('signup'))
    if register(request.args['username'], request.args['password']): #successful registration
        session["userID"] = True
        session["currentID"] = request.args['username']
        session["error"] = False
        return redirect(url_for("home"))

# homepage
@app.route("/home")
def home():
    if not checkAuth():
        return redirect(url_for('login'))
    # loading dog API
    url = "https://random.dog/woof.json"
    response = urllib.request.urlopen(url)
    response = response.read()
    data = json.loads(response)
    while (data['url'][-1] == '4'): # mp4s are not displayable
        response = urllib.request.urlopen(url)
        response = response.read()
        data = json.loads(response)
    return render_template('home.html', dog=data['url'], error=session["error"], message=session["message"])

# account settings page
@app.route("/settings")
def settings():
    print(session["e1"], session["e2"], session["message"])
    if not checkAuth():
        return redirect(url_for('login'))
    return render_template('settings.html', e1 = session["e1"], e2 = session["e2"], message=session["message"]);

# request to change account settings
@app.route("/change_settings")
def changing():
    session["e1"] = False
    session["e2"] = False
    print(get("users", "*", ""))
    if not checkAuth():
        return redirect(url_for('login'))
    # no password stuff entered --> change Username
    if (request.args['check_password'] == ''):
        if (request.args['new_password'] != '' or request.args['confirm_password'] != ''): #if other password fields filled out, something's wrong
            session["e2"] = True
            session["message"]="Necessary Fields Not Filled Out"
            return redirect(url_for('settings'))
        # change Username
        if (request.args['newusername'] == ''): #if username fields not filled out, something's wrong
            session["e1"] = True
            session["message"]="Necessary Fields Not Filled Out"
            return redirect(url_for('settings'))
        if (get("users", "username", "WHERE username = '%s'" % request.args['newusername']) != []): #username is in database already
            session["e1"] = True
            session["message"]="Username Already Taken"
            return redirect(url_for('settings'))
        update_user(session['currentID'], "username", request.args['newusername']) #updating the database imported
        session["currentID"] = request.args['newusername']
        return render_template('settings.html', changed1=True)
    else: # password being changed
        if (request.args['new_password'] == '' or request.args['confirm_password'] == ''): #if password fields not filled out, something's wrong
            session["e2"] = True
            session["message"]="Necessary Fields Not Filled Out"
            return redirect(url_for('settings'))
        if (request.args['check_password'] != get("users", "hashpassword", "WHERE username = '%s'" % session['currentID'])[0][0]): #old password not correct
            session["e2"] = True
            session["message"]="Incorrect Password"
            return redirect(url_for('settings'))
        if (request.args['new_password'] != request.args['confirm_password']): #passwords don't match
            session["e2"] = True
            session["message"]="Passwords Don't Match"
            return redirect(url_for('settings'))
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
    if not checkAuth():
        return redirect(url_for('login'))
    #blah = get("countries", "code", "WHERE name == '%s'" % request.args['query'])[0][0]
    #print(blah)
    #return "poo"
    #session['countrycode'] = countries[request.args['query']]
    #session['country'] = request.args['query']
    country = comparecountry(request.args['query'].lower(), countries)
    if country == "BOO":
        session["error"] = True
        return redirect(url_for('home'))
    session["error"] = False
    username = session["currentID"]
    print(username)
    userID = get("users", "userid", "WHERE username = '%s'" % username)[0][0]
    print(userID)
    update_searches(userID, country)
    session['countrycode'] = countries[country]
    session['country'] = country
    return render_template('searchedcountry.html', country = country)

# search page for a country and category
@app.route("/search/<category>")
def fullsearch(category):
    if not checkAuth():
        return redirect(url_for('login'))
    articles = newsapi(session['countrycode'], category)
    newarticles = newyorktimesapi(session['country'], category)
    guardian = guardianapi(session['country'], category)
    #print(guardian)
    #print(newarticles)
    return render_template('results.html',
                            category = category,
                            country = session['country'].capitalize(),
                            articles = articles,
                            newarticles = newarticles,
                            guardian = guardian)

if __name__ == "__main__":
    app.debug = True
    app.run()
