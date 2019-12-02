# RedDacks: Nahi Khan, Grace Mao, Sophie Nichol, Jackson Zou
# SoftDev1 pd9
# P01
# 2019-11-21

from flask import Flask, render_template, request, redirect, url_for, session, flash
from utl.db import insert, get, setup, update_user
from utl.auth import auth, checkAuth, register
from utl.apistuff import newsapi, pullcountries, newyorktimesapi
import urllib.request, json, sqlite3, os

app = Flask(__name__)
app.secret_key = "Dacks"

setup()
countries = pullcountries()

@app.route("/")
def root():
    if checkAuth(): #if you've already logged in
        return redirect(url_for('home'))
    else: #if not, redirect to login page
        return redirect(url_for('login'))

@app.route("/login") #login page
def login():
    if checkAuth():
        return redirect(url_for('home'))
    else:
        return render_template('login.html')

@app.route("/signup") #signup page
def signup():
    if checkAuth():
        return redirect(url_for('home'))
    return render_template('signup.html')

@app.route("/auth")
def authen():
    if auth(request.args['username'], request.args['password']):
        session["userID"] = True
        session["currentID"] = request.args['username']
        return redirect(url_for('home'))
    if get("users", "username", "WHERE username = '%s'" % request.args['username']):
        return render_template('login.html', error=True, message='Password Incorrect')
    return render_template('login.html', error=True, message='Username Not Found')

@app.route("/register")
def reg():
    #print(request.args['username'])
    #print(get("users", "username", "WHERE username = '%s'" % request.args['username'])[0][0])
    #print(request.args['username']==get("users", "username", "WHERE username = '%s'" % request.args['username'])[0][0])
    if (request.args['password'] != request.args['password2']):
        return render_template('signup.html', error=True, message="Passwords Don't Match")
    if (request.args['username'] == get("users", "username", "WHERE username = '%s'" % request.args['username'])):
        return render_template('signup.html', error=True, message="Username Already Taken")
    if register(request.args['username'], request.args['password']):
        session["userID"] = True
        return redirect(url_for("home"))

@app.route("/home")
def home():
    url = "https://random.dog/woof.json"
    response = urllib.request.urlopen(url)
    response = response.read()
    data = json.loads(response)
    while (data['url'][-1] == '4'):
        response = urllib.request.urlopen(url)
        response = response.read()
        data = json.loads(response)
    return render_template('home.html', dog=data['url'])

@app.route("/settings")
def settings():
    return render_template('settings.html');

@app.route("/change_settings")
def changing():
    # no password stuff entered --> change Username
    if (request.args['check_password'] == ''):
        if (request.args['new_password'] != '' or request.args['confirm_password'] != ''):
            return render_template('settings.html', error2=True, message="Necessary Fields Not Filled Out")
        # change Username
        if (request.args['newusername'] == ''):
            return render_template('settings.html', error1=True, message="Necessary Fields Not Filled Out")
        if (request.args['newusername'] == get("users", "username", "WHERE username = '%s'" % request.args['newusername'])[0][0]):
            return render_template('settings.html', error1=True, message="Username Already Taken")
        update_user(session['currentID'], "username", request.args['newusername'])
        return render_template('settings.html', changed1=True)
    else: # password being changed
        if (request.args['new_password'] == '' or request.args['confirm_password'] == ''):
            return render_template('settings.html', error2=True, message="Necessary Fields Not Filled Out")
        #print("-----------------")
        #print(get("users","hashpassword","WHERE username='%s'" % session['currentID']))
        if (request.args['check_password'] != get("users", "hashpassword", "WHERE username = '%s'" % session['currentID'])[0][0]):
            return render_template('settings.html', error2=True, message="Incorrect Password")
        if (request.args['new_password'] != request.args['confirm_password']):
            return render_template('settings.html', error2=True, message="Passwords Don't Match")
        update_user(session['currentID'], "hashpassword", request.args['new_password'])
        return render_template('settings.html', changed2=True)


@app.route("/logout")
def logout():
    session.pop("userID")
    return redirect("/")

@app.route("/search")
def search():
    #blah = get("countries", "code", "WHERE name == '%s'" % request.args['query'])[0][0]
    #print(blah)
    #return "poo"
    session['countrycode'] = countries[request.args['query'].lower()]
    session['country'] = request.args['query']
    return render_template('searchedcountry.html')

@app.route("/search/<category>")
def fullsearch(category):
    articles = newsapi(session['countrycode'], category)
    newarticles = newyorktimesapi(session['country'], category)
    #print(newarticles)
    return render_template('results.html', category = category, country = session['country'].capitalize(), articles = articles, newarticles = newarticles)

if __name__ == "__main__":
    app.debug = True
    app.run()
