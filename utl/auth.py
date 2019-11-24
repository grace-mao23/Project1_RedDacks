# Standard Lib
from flask import session
from utl.db import insert, get

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
        insert("users", ["NULL", username, password, username])
    return True

def checkAuth():
    if "userID" in session:
        return True
    else:
        return False
