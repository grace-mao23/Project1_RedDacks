# RedDacks: Nahi Khan, Grace Mao, Sophie Nichol, Jackson Zou
# SoftDev1 pd9
# P01
# 2019-11-21

from flask import Flask, render_template, request, redirect, url_for, session, flash
from utl.db import insert, get, setup
from utl.auth import auth, checkAuth, register
from utl.apistuff import newsapi, pullcountries
import urllib.request, json, sqlite3, os

app = Flask(__name__)
app.secret_key = "Dacks"

@app.route("/")
def root():
    setup()
    pullcountries()
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

@app.route("/logout")
def logout():
    session.pop("userID")
    return redirect("/")

@app.route("/search")
def search():
    #blah = get("countries", "code", "WHERE name == '%s'" % request.args['query'])[0][0]
    #print(blah)
    #return "poo"
    countries = pullcountries()
    print(countries)
    articles = newsapi(countries[request.args['query']])
    return render_template('searchedtopics.html', articles = articles)

if __name__ == "__main__":
    app.debug = True
    app.run()
