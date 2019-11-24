from flask import Flask, render_template, request, redirect, url_for
import urllib.request, json
from utl.db import insert, get

# should take in the countryID
def newsapi(location):
    u = urllib.request.urlopen("https://newsapi.org/v2/top-headlines?country={}&apiKey=6b19e4b53ded4360bec67947b47a27de".format(location))
    response = u.read()
    data = json.loads(response)
    articles = data["articles"]
    numarticles = 0
    final = []

    if data["totalResults"] > 5:
        numarticles = 5
    else:
        numarticles = data["totalResults"]

    final.append(numarticles)
    for i in range(0,numarticles):
        l = articles[i]
        temp = []
        temp.append(l["title"])
        temp.append(l["author"])
        temp.append(l["description"])
        temp.append(l["url"])
        temp.append(l["urlToImage"])
        final.append(temp)
        # add results to database
        insert("news", ["NULL", location, l["title"], l["author"], l["description"], l["url"], l["urlToImage"], "NULL"])

    return final

def newyorktimesapi(location):
    u = "https://api.nytimes.com/svc/search/v2/articlesearch.json?api-key=EXwPWJTDhL7IfXGSRFvCDNMHYclouOYM&sort=newest&fq=unitedstates&facet_filter=true"

def getlocation(location):
    if location.lower() == "united states":
        location = "us"
    try:
        u = urllib.request.urlopen("https://restcountries.eu/rest/v2/name/{}?fullText=true".format(location))
    except:
        return "Bad value for location"
    response = u.read()
    data = json.loads(response)
    # add to database
    insert("countries", ["NULL", data[0]['alpha2Code'], location])
    return data[0]['alpha2Code']
