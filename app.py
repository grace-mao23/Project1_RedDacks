# RedDacks: Nahi Khan, Grace Mao, Sophie Nichol, Jackson Zou
# SoftDev1 pd9
# P01
# 2019-11-21

from flask import Flask, render_template, request, redirect, url_for, session, flash
from utl.db import insert, get, setup
import urllib.request, json, sqlite3, os

app = Flask(__name__)
app.secret_key = "Dacks"

setup()

def auth(username, password):
    try:
        pword = get("users", "hashpassword",
                           "WHERE username = '%s'" % username)[0][0]
        if pword == password:
            return True
    except:
        return False

def register(username, password):
    if not auth(username, password):
        insert("users", ["NULL", username, password])
    return True

def checkAuth():
    if "userID" in session:
        return True
    else:
        return False

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
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route("/register")
def reg():
    if (request.args['username'] == ""):
        return redirect("/")
    if (request.args['password'] == ""):
        return redirect("/")
    if (request.args['password'] != request.args['password2']):
        return redirect("/")
    if (get("users", "username", "WHERE username = '%s'" % request.args['username'])):
        return redirect("/")
    if register(request.args['username'], request.args['password']):
        session["userID"] = True
        return redirect(url_for("home"))

@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/logout")
def logout():
    session.pop("userID")
    return redirect("/")

if __name__ == "__main__":
    app.debug = True
    app.run()
