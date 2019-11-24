from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

@app.route('/')
def search():
  return render_template("SearchPage.html")

@app.route('/searchresults', methods = ['POST','GET'])
def results():
    names = {}
    #yelp api
    api_key = "yA-Y1rmv7amNieFCPoifXHgXFuKmBzrUQw34HR9c-3eUW84SwA0kMUZkJ04trBfHDNiP2WM9-HpRZqCC5qR889uO2k38RnV_Z1RN4WeycS1pbDtq2A9TEZDmnvfTXXYx"
    headers = {"Authorization": "Bearer %s" % api_key}
    searchKey = request.form.get("searchKey")
    url = ("https://api.yelp.com/v3/businesses/search")
    params = {'term':'restaurant','location':searchKey}
    req = requests.get(url, params=params, headers=headers)
    # proceed only if the status code is 200
    print('The status code is {}'.format(req.status_code))
    
    # printing the text from the response 
    parsed = json.loads(req.text)
    businesses = parsed["businesses"]
    yelpRating = []
    yelpAddress = []
    yelpPhone = []
    for business in businesses:
      if business["name"] in names:
        names[business["name"]].append("Yelp review: " + str(business["rating"]))
      else:
        names[business["name"]] = ["Yelp review: " + str(business["rating"])]
      yelpRating.append(business["rating"])
      yelpAddress.append( " ".join(business["location"]["display_address"]))
      yelpPhone.append(business["phone"])    
    
    #google api
    api_key = "AIzaSyCZaW4zZYWR1ghHtn6jAIdVSJzWw7YVXxI"
    url = ("https://maps.googleapis.com/maps/api/place/findplacefromtext/json?")
    for key in names:
      print(key)
      params = {'input': key.lower() + " " + searchKey, 'inputtype':'textquery', 'fields':'name,rating','key':api_key}
      req = requests.get(url, params=params)
      # proceed only if the status code is 200
      print('The status code is {}'.format(req.status_code))
    
      # printing the text from the response
      parsed = json.loads(req.text)
      businesses = parsed["candidates"]
      for business in businesses:
        if(len(names[key]) <2):
          names[key].append("Google review: " + str(business["rating"]))
          break
  
    
    return render_template("results.html", searchKey=searchKey, names = names, yelpAddress = yelpAddress, yelpPhone = yelpPhone)
  

