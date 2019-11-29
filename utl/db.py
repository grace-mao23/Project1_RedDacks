# Standard Lib
import sqlite3
from sqlite3 import connect
from re import search
from numbers import Number
# Flask Lib
from flask import current_app, g
#from utl.apistuff import pullcountries

DB_FILE = "data/database.db"

def setup():
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
                userid INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                hashpassword TEXT NOT NULL,
                displayname TEXT NOT NULL
                );""")
    c.execute("""DROP TABLE IF EXISTS countries;""")
    c.execute("""CREATE TABLE IF NOT EXISTS countries(
            	countryID INTEGER PRIMARY KEY AUTOINCREMENT,
            	code TEXT NOT NULL,
            	name TEXT NOT NULL
            	);""")
    c.execute("""CREATE TABLE IF NOT EXISTS news(
                articleID INTEGER PRIMARY KEY AUTOINCREMENT,
                countryID INTEGER,
				title TEXT NOT NULL,
				author TEXT NOT NULL,
                description TEXT,
				url TEXT NOT NULL,
				imageURL TEXT NOT NULL,
                dateandtime TEXT,
                FOREIGN KEY (countryID) REFERENCES countries (countryID)
                );""")
                #should I change timeanddate to timesstamp? ^
    c.execute("""CREATE TABLE IF NOT EXISTS NYTimes(
                nytID INTEGER PRIMARY KEY AUTOINCREMENT,
                countryID INTEGER,
				title TEXT NOT NULL,
				author TEXT NOT NULL,
                description TEXT,
				url TEXT NOT NULL,
				imageURL TEXT NOT NULL,
                timepulled TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (countryID) REFERENCES countries (countryID)
                );""")
    c.execute("""CREATE TABLE IF NOT EXISTS Keys(
                name TEXT NOT NULL,
                apikey TEXT NOT NULL
                );""")
    c.close()
    #pullcountries

# Return the column types of a table
def header_types(tbl_name):
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()
    c.execute("PRAGMA TABLE_INFO (%s)" % (tbl_name))
    heads = c.fetchall()
    c.close()
    return [str(head[1]) for head in heads]


# Insert a row into a table given the values
def insert(tbl_name, values):
    try:
        db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
        c = db.cursor()
        data_string = ""
        for value in values:
            if isinstance(value, Number) or bool(search("^[+-]?([0-9]+([.][0-9]*)?|[.][0-9]+)$", value)):
                data_string += str(value) + ","
            elif value == "datetime('now')" or value == "NULL":
                data_string += value + ","
            else:
                data_string += "'%s'," % value
        c.execute("INSERT INTO %s VALUES (%s)" %
                    (tbl_name, data_string[:-1]))
        db.commit()
        c.close()
        return True
    except:
        return False

def insertCountry(ccode, cname):
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()
    c.execute("INSERT into countries (code, name) VALUES(?, ?);", (ccode, cname))
    #c.execute("INSERT into countries VALUES(NULL, ?, ?);", (ccode, cname))
    db.commit()
    c.close()

def get(tbl_name, column, conditional=""):
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()
    c.execute("SELECT %s FROM %s %s" % (column, tbl_name, conditional))
    values = c.fetchall()
    c.close()
    return [list(value) for value in values]

def update_user(username, field, newvalue):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("UPDATE users SET %s = '%s' WHERE username = '%s'" % (
                field,
                newvalue,
                username
            )
        )
    db.commit()
    c.close()
    return "Success"
