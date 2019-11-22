#
# SoftDev1 PD 9
# P01
# 11/13/2019

from flask import Flask, render_template, request, redirect, url_for, session, flash

import urllib.request, json, sqlite3, os

app = Flask(__name__)



def checkAuth():
    if "userID" in session:
        return True
    else:
        return False

@app.route("/")
def root():
    if checkAuth(): #if you've already logged in
        return redirect(url_for('homeb'))
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




if __name__ == "__main__":
    app.debug = True
    app.run()
