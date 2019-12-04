# Standard Lib
from flask import session
from utl.db import insert, get

"""
    This module deals with sessions and whether users are logged in
"""

# checking if the username and password are valid
def auth(username, password):
    try:
        pword = get("users", "hashpassword",
                           "WHERE username = '%s'" % username)[0][0]
        if pword == password:
            return True
    except:
        return False

# updating the database for new users
def register(username, password):
    if not auth(username, password):
        insert("users", ["NULL", username, password, username])
        userID = get("users", "userID", "WHERE username = '%s'" % username)[0][0]
        # putting in NULL searches for users so that recent searches will have something
        insert("searches", ["NULL", "NULL", 1, userID])
        insert("searches", ["NULL", "NULL", 2, userID])
        insert("searches", ["NULL", "NULL", 3, userID])
        insert("searches", ["NULL", "NULL", 4, userID])
        insert("searches", ["NULL", "NULL", 5, userID])
    return True

# checking if a user is logged in
def checkAuth():
    if "userID" in session:
        if session["userID"]:
            return True
    else:
        return False
