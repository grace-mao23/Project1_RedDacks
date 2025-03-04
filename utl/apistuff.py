from flask import Flask, render_template, request, redirect, url_for
import urllib.request, json
from utl.db import get, insertCountry, insert

"""
    This module contains all things related to our APIs
    It mainly runs the search engine
"""

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
    index = 0
    for l in results:
        if index == 5:
            break
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
        index+=1
    return final

# the guardian API
def guardianapi(country, category):
    country = country.lower()
    # conversions to match the guardian API system
    if country == "united states of america":
        country = "us"
    if country == "united kingdom of great britain and northern ireland":
        country = "britain"
    if country == "bolivia (plurinational state of)":
        country = "bolivia"
    if country == "bosnia and herzegovina":
        country = "bosnia"
    if country == "lao people's democratic republic":
        country = "lao"
    if country == "macedonia (the former yugoslav republic of)":
        country = "macedonia"
    if country == "micronesia (federated states of)":
        country = "micronesia"
    if country == "moldova (republic of)":
        country = "moldova"
    if country == "korea (democratic people's republic of)":
        country = "korea"
    if country == "palestine, state of":
        country = "palestine"
    if country == "republic of kosovo":
        country = "kosovo"
    if country == "syrian arab republic":
        country = "syria"
    if country == "venezuela (bolivarian republic of)":
        country = "venezuela"
    country = country.replace(" ","")
    print(country)
    if category == "entertainment":
        category = "fashion"
    u = ""
    if category == "sports":
        u = urllib.request.urlopen("https://content.guardianapis.com/search?q={}&tag=theguardian/mainsection/sport&api-key=e7b0c4b8-b09e-43a3-b5c7-00898671b7de".format(country))
        print("u1")
    if category == "health":
        u = urllib.request.urlopen("https://content.guardianapis.com/search?q={}&tag=society/health&api-key=e7b0c4b8-b09e-43a3-b5c7-00898671b7de".format(country))
        print("u2")
    if category == "general":
        u = urllib.request.urlopen("https://content.guardianapis.com/search?q={}&api-key=e7b0c4b8-b09e-43a3-b5c7-00898671b7de".format(country))
        print("u3")
    else:
        u = urllib.request.urlopen("https://content.guardianapis.com/search?q={}&tag={}/{}&api-key=e7b0c4b8-b09e-43a3-b5c7-00898671b7de".format(country, category, category))
        print("u4")
    response = u.read()
    data = json.loads(response)
    #print(data)
    articles = data["response"]["results"]
    final = []
    index = 0
    for article in articles:
        if index == 5:
            break
        temp = []
        temp.append(article["webTitle"])
        temp.append(article["webUrl"])
        final.append(temp)
        index+=1
    return final

# initial setup of the country table to obtain country codes etc
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

# string converter to take in strange requests for countries
def comparecountry(newcountry, countries):
    compares = {}
    compares[""] = 0
    for country in countries:
        score = 0
        countrylist = country.split(" ")
        n = newcountry.split(" ")
        for word in countrylist:
            for nword in n:
                if word == nword:
                    score += 1
        if score > 0:
            compares[country] = score
    keys = compares.keys()
    #print(keys)
    if len(keys) == 1:
        return "BOO"
    final = ""
    for country in keys:
        if compares[country] > compares[final]:
            final = country
        if compares[country] == compares[final]:
            if len(final.split(" ")) > len(country.split(" ")):
                final = country
    return final
