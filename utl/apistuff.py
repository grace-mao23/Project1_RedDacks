from flask import Flask, render_template, request, redirect, url_for
import urllib.request, json

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
        final.append(temp)
    return final
