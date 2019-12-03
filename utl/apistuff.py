from flask import Flask, render_template, request, redirect, url_for
import urllib.request, json
from utl.db import get, insertCountry, insert

# should take in the countryID
"""
    loads search results from the News API
    pulls at most 5 articles due to the large quantity of articles in the News API database
    displays title, author, description, a hyperlink to the article, and a hyperlink to the article's image
"""
def newsapi(location, category):
    u = urllib.request.urlopen("https://newsapi.org/v2/top-headlines?country={}&category={}&apiKey=6b19e4b53ded4360bec67947b47a27de".format(location, category))
    response = u.read()
    data = json.loads(response)
    articles = data["articles"]
    numarticles = 0
    final = []

    if data["totalResults"] > 5:
        numarticles = 5
    else:
        numarticles = data["totalResults"]

    #final.append(numarticles)
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
        #insert("news", ["NULL", location, l["title"], l["author"], l["description"], l["url"], l["urlToImage"], "NULL"])

    return final

"""
    similar to above, but for the New York Times API
"""
def newyorktimesapi(country, category):
    #business = business
    #science = science
    #entertainment = fashion / magazine
    #general = sundayreview
    #health = health
    #sports = sports
    #technology = technology
    if category.lower() == "general":
        category = "sundayreview"
    if category.lower() == "entertainment":
        category = "fashion"
    u = urllib.request.urlopen("https://api.nytimes.com/svc/topstories/v2/{}.json?api-key=EXwPWJTDhL7IfXGSRFvCDNMHYclouOYM".format(category))
    response = u.read()
    data = json.loads(response)
    results = data["results"]
    final = []
    for l in results:
        countries = l["geo_facet"]
        for place in countries:
            if place.lower() == country:
                temp = []
                temp.append(l["title"])
                temp.append(l["byline"])
                temp.append(l["abstract"])
                temp.append(l["url"])
                if len(l["multimedia"]) > 0:
                    temp.append(l["multimedia"][0]["url"])
                else:
                    temp.append("None")
                final.append(temp)
        if len(countries) == 0:
            temp = []
            temp.append(l["title"])
            temp.append(l["byline"])
            temp.append(l["abstract"])
            temp.append(l["url"])
            if len(l["multimedia"]) > 0:
                temp.append(l["multimedia"][0]["url"])
            else:
                temp.append("None")
            final.append(temp)
    return final

def guardianapi(category):
    u = urllib.request.urlopen("https://content.guardianapis.com/environment?api-key=e7b0c4b8-b09e-43a3-b5c7-00898671b7de")
    response = u.read()
    data = json.loads(response)

def pullcountries():
    u = urllib.request.urlopen("https://restcountries.eu/rest/v2/all")
    response = u.read()
    data = json.loads(response)
    final = {}
    for country in data:
        final[country["name"].lower()] = country["alpha2Code"]
        insertCountry(country['alpha2Code'], country["name"])
    return final

# def getlocation(location):
#     if location.lower() == "united states":
#         location = "us"
#     try:
#         u = urllib.request.urlopen("https://restcountries.eu/rest/v2/name/{}?fullText=true".format(location))
#     except:
#         return "Bad value for location"
#     response = u.read()
#     data = json.loads(response)
#     # add to database
#     insert("countries", ["NULL", data[0]['alpha2Code'], location])
#     return data[0]['alpha2Code']
