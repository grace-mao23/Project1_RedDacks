#
# SoftDev1 PD 9
# P01
# 11/13/2019

from flask import Flask, render_template, request, redirect, url_for
import urllib.request, json
app = Flask(__name__)

@app.route("/")
def helloworld():
    return "bing bong"

if __name__ == "__main__":
    app.debug = True
    app.run()
