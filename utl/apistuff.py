from flask import Flask, render_template, request, redirect, url_for
import urllib.request, json
#from utl.db import insert, get
from db import insert, get

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

def newyorktimesapi(category):
    u = urllib.request.urlopen("https://api.nytimes.com/svc/topstories/v2/{}.json?api-key=EXwPWJTDhL7IfXGSRFvCDNMHYclouOYM".format(category))
    response = u.read()
    data = json.loads(response)
    results = data["results"]
    final = []
    for l in results:
        temp = []
        temp.append(l["title"])
        temp.append(l["byline"])
        temp.append(l["abstract"])
        temp.append(l["url"])
        temp.append(l["multimedia"][0]["url"])
        final.append(temp)
    return final

def guardianapi(category):
    u = urllib.request.urlopen("https://content.guardianapis.com/environment?api-key=e7b0c4b8-b09e-43a3-b5c7-00898671b7de")
    response = u.read()
    data = json.loads(response)

# def calenderapi(location):
#     u = urllib.request.urlopen("https://calendarific.com/api/v2/holidays?api_key=afae9c6e72a9f688537453a3fafc6ce35b12e0ad&country=US&year=2019&type=national")
#     response = u.read()
#     data = json.loads(response)
#     print(data)
#     # data = data["response"]["holidays"]
#     # final = []
#     # for i in range(0, 5):
#     #     temp = []
#     #     temp.append(i["name"])
#     #     temp.append(i["description"])
#     #     temp.append(i["date"]["iso"])
#     #     final.append(temp)
#     # return final


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

print(newyorktimesapi("science"))
