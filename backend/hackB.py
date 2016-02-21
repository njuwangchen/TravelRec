
# coding: utf-8

# In[1]:

import requests, json
from math import radians, cos, sin, asin, sqrt
from datetime import datetime
import random
import time
import cPickle as pickle
import xgboost as xgb
import pandas as pd
#import numpy as np
#import matplotlib.pyplot as plt
#import seaborn as sns
import operator


# In[2]:

# REQUEST POINT OF INTEREST
def requestPoints(city_name):
    search_type = "points-of-interest/yapq-search-text"
    number = 10
    params = "city_name=%s&number_of_images=1&number_of_results=%d" % (city_name, number)
    url = "%s/%s?apikey=%s&%s" % (base, search_type, apikey, params)
    js = json.loads(sess.get(url).text)  
    return js

#requestPoints("Chicago")


# In[3]:

# REQUEST FLIGHT
def requestFlights(origin, dest, start_date, end_date, budget):
    search_type = "flights/low-fare-search"
    number = 5
    params = "origin=%s&destination=%s&departure_date=%s&return_date=%s&max_price=%d&currency=USD&adults=1&non_stop=true&number_of_results=%d" % (origin, dest, start_date, end_date, budget, number)
    url = "%s/%s?apikey=%s&%s" % (base, search_type, apikey, params)
    js = json.loads(sess.get(url).text)
    return js

#requestFlights("BOS", "CHI", "2016-06-01", "2016-06-05", 10000)


# In[4]:

# REQUEST HOTELS NEAR THE AIRPORT 
def requestAirportHotels(dest, start_date, end_date, budget):
    search_type = "hotels/search-airport"
    number = 10
    day = abs((datetime.strptime(start_date, "%Y-%m-%d") - datetime.strptime(end_date, "%Y-%m-%d")).days)
    params = "location=%s&check_in=%s&check_out=%s&max_rate=%f&number_of_results=%d&currency=USD" %                 (dest, start_date, end_date, budget/float(day), number)
    url = "%s/%s?apikey=%s&%s" % (base, search_type, apikey, params)
    js = json.loads(sess.get(url).text)
    return js

#requestAirportHotels("BOS", "2016-06-01", "2016-06-05", 10000)


# In[5]:

# REQUEST GEO HOTELS
def requestGeoHotels(latitude, longitude, radius, start_date, end_date, budget):
    search_type = "hotels/search-circle"
    number = 10
    day = abs((datetime.strptime(start_date, "%Y-%m-%d") - datetime.strptime(end_date, "%Y-%m-%d")).days)
    params = "latitude=%f&longitude=%f&radius=%f&check_in=%s&check_out=%s&currency=USD&max_rate=%f&number_of_results=%d" %                 (latitude, longitude, radius, start_date, end_date, budget/float(day), number)
    url = "%s/%s?apikey=%s&%s" % (base, search_type, apikey, params)    
    js = json.loads(sess.get(url).text)
    return js

#print requestAirportHotels(36.0857, -115.1541, 42, "2016-06-14", "2016-06-16", 200)


# In[6]:

# REQUEST TOP DEST
def requestTopDests(origin, date, number):
    search_type = "travel-intelligence/top-destinations" 
    params = "period=%s&origin=%s&number_of_results=%d" % (date, origin, number)
    url = "%s/%s?apikey=%s&%s" % (base, search_type, apikey, params)
    js = json.loads(sess.get(url).text)
    return js

#print requestTopDests("BOS", "2015-01", 10)


# In[7]:

# REQUEST TOP SEARCHES
def requestTopSearches(origin, date, number):
    search_type = "travel-intelligence/top-searches" 
    params = "period=%s&origin=%s&country=US&number_of_results=%d" % (date, origin, number)
    url = "%s/%s?apikey=%s&%s" % (base, search_type, apikey, params)
    js = json.loads(sess.get(url).text)
    return js

#print requestTopSearches("BOS", "2015-01", 10)


# In[8]:

# REQUEST INSPIRATION FLIGHT
def requestInspirFlight(origin, date0, date1, budget, number):
    search_type = "flights/inspiration-search"
    params = "origin=%s&departure_date=%s--%s&max_price=%s" % (origin, date0, date1, budget)
    url = "%s/%s?apikey=%s&%s" % (base, search_type, apikey, params)
    js = json.loads(sess.get(url).text)
    return js

#print requestInspirFlight("BOS", "2016-06-14", "2016-06-16", 300, 10)


# In[9]:

# REQUEST CODE TO CITY
def requestCodeToCity(city_code):
    if (city_code == "WAS"):
        return "Washington"
    url = "%s/location/%s?apikey=%s" % (base, city_code, apikey)
    js = json.loads(sess.get(url).text)
    #print "city_code = ", city_code
    return js["airports"][0]["city_name"]

#print requestCodeToCity("BOS")


# In[10]:

# REQUEST POINT OF INTEREST
def requestPoints(city_name):
    search_type = "points-of-interest/yapq-search-text"
    number = 10
    params = "city_name=%s&number_of_images=1&number_of_results=%d" % (city_name, number)
    url = "%s/%s?apikey=%s&%s" % (base, search_type, apikey, params)
    #print "city_name = ", city_name
    js = json.loads(sess.get(url).text)
    return js

#requestPoints("Chicago")


# In[11]:

# GENERATE CANDIDATE LIST
def candidatesList(origin, date0, date1, budget):
    candidates = set()
    l = requestTopDests(origin, "2015-" + date0.split("-")[1], 10)
    if (l.has_key("results") == True):
        candidates = candidates | {x["destination"] for x in l["results"]}
    l = requestTopSearches(origin, "2015-" + date0.split("-")[1], 5)
    if (l.has_key("results") == True):
        candidates = candidates | {x["destination"] for x in l["results"]}
    l = requestInspirFlight(origin, date0, date1, budget, 10)
    if (l.has_key("results") == True):
        candidates = candidates | {x["destination"] for x in l["results"][:15]}
    candidates &= support_code
    return candidates

#print candidatesList("BOS", "2016-06-01", "2016-06-17", 1000)"2015-" + date0.split("-")[1]


# In[13]:

# CALCULATE DISTANCE
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r


# In[14]:

# CALCULATE SCORES - linear method
def calulateScoreLinear(feature):
    feature['average_rate'] = feature['average_rate'] / 5       # 0.2
    feature['central_dst']  = 1 - feature['central_dst'] / 50   # 0.2
    feature['flight_price'] = 1 - feature['flight_price']       # 0.1
    feature['hotel_price']  = 1 - feature['hotel_price']        # 0.1
    feature['total_price']  = 1 - feature['average_rate']       # 0.3
    feature['nonstop']      = feature['nonstop']                # 0.1
    
    return feature['average_rate'] * 0.2 + feature['central_dst'] * 0.2 + feature['flight_price'] * 0.2         + feature['hotel_price'] * 0.1 + feature['total_price'] * 0.3 + feature['nonstop'] * 0.1
    
    #return random.random()


# In[15]:

# CALCULATE SCORES - xgb model
#def calulateScoreXGB(feature):
def calulateScore(feature):
    feature['average_rate'] = feature['average_rate'] / 5       # 0.2
    feature['central_dst']  = 1 - feature['central_dst'] / 50   # 0.2
    feature['flight_price'] = 1 - feature['flight_price']       # 0.1
    feature['hotel_price']  = 1 - feature['hotel_price']        # 0.1
    feature['total_price']  = 1 - feature['average_rate']       # 0.3
    feature['nonstop']      = feature['nonstop']                # 0.1
    
    feature_list = [feature]
    testData = pd.DataFrame(feature_list)
    predicted = xg.predict(xgb.DMatrix(testData[select_features]))
    return predicted[0]

    #return random.random()


# In[16]:

def testXGBPredict():
    feature = {}
    feature['average_rate'] = 4.5
    feature['central_dst']  = 30
    feature['flight_price'] = 0.5
    feature['hotel_price']  = 0.4
    feature['total_price']  = 0.9
    feature['nonstop']      = 0
    print calulateScoreXGB(feature)

#testXGBPredict()


# In[17]:

def getScoreList(origin, start_date, end_date, budget):
    dest_list = candidatesList(origin, start_date, end_date, budget)
    print "dest_list = ", dest_list
    
    dest_score_list = []   
    for dest in dest_list:
        print "current dest = ", dest
        
        # REQUEST POINTS OF INTERTES
        point_js = poi_dict[dest]
        if (point_js.has_key("points_of_interest") == False or len(point_js["points_of_interest"]) == 0):
            print "num of points_of_interest = 0"
            continue
        else: print "num of points_of_interest = ", len(point_js["points_of_interest"])
        
        l = reduce(lambda (n1, r1, lo1, la1),(n2, r2, lo2, la2): (n1 + n2, r1 + r2, lo1 + lo2, la1 + la2),                    map(lambda x: (1, float(x["grades"]["yapq_grade"]), float(x["location"]["longitude"]),                                 float(x["location"]["latitude"])), point_js["points_of_interest"]))
        average_rate = l[1] / l[0]
        average_lo   = l[2] / l[0]
        average_la   = l[3] / l[0]
        
        # REQUEST HOTEL INFO
        hotel_js = requestGeoHotels(average_la, average_lo, 50, start_date, end_date, budget)
        if (hotel_js.has_key("results") == False or len(hotel_js["results"]) == 0):
            print "num of hotels = 0"
            continue
        else: print "num of hotels = ", len(hotel_js["results"])
        
        # REQUEST FLIGHT INFO
        flight_js = requestFlights(origin, dest, start_date, end_date, budget)
        if (flight_js.has_key("results") == False or len(flight_js["results"]) == 0):
            print "num of flight = 0"
            continue
        else: print "num of flight = ", len(flight_js["results"])
        
        score_list = []
        for flight in flight_js["results"]:
            flightID = "origin=%s,dest=%s,start_date=%s,end_date=%s,outbound=%s,inbound=%s"                % (origin, dest, start_date, end_date, flight["itineraries"][0]["outbound"]["flights"][0]["aircraft"],                  flight["itineraries"][0]["inbound"]["flights"][0]["aircraft"])
            #print "flightID =", flightID
            flight_dict[flightID] = flight
            
            for hotel in hotel_js["results"]:
                hotelID = "dest=%s,start_date=%s,end_date=%s,property_code=%s"                % (dest, start_date, end_date, hotel["property_code"])
                #print "hotelID =", hotelID
                hotel_dict[hotelID] = hotel
                
                feature = {}
                
                # flight feature
                feature["flight_price"] = float(flight["fare"]["total_price"]) / budget
                if (len(flight["itineraries"][0]["inbound"]["flights"]) != 1 or                   len(flight["itineraries"][0]["outbound"]["flights"]) != 1):
                    feature["nonstop"] = 0
                else: feature["nonstop"] = 1
                
                # hotel feature
                feature["hotel_price"] = float(hotel["total_price"]["amount"]) / budget 
                
                # point feature
                feature["average_rate"] = average_rate

                # combination feature
                feature["total_price"] = 1 - (feature["flight_price"] + feature["hotel_price"])
                if feature["total_price"] > 1:
                    continue
                feature["central_dst"] = 50 - haversine(average_lo, average_la, float(hotel["location"]["longitude"]),                                         float(hotel["location"]["latitude"]))
                        
                # Calculate Score
                score = calulateScore(feature)
                score_list.append((score, flightID, hotelID))
                
                #print "feature = ", feature
                #print "score = ", score
    
        score_list = sorted(score_list, key=lambda score: score[0], reverse = True)
        if (len(score_list) > 0):
            # print "score_list = ", score_list
            ret = (score_list[0][0], dest, [score_list[i] for i in range(min(3, len(score_list)))])
            # print ret
            dest_score_list.append(ret)
            #return 0
        else:
            print "Warning : len(score_list) == 0 ?"
            print "Warning : num of points_of_interest = ", len(point_js["points_of_interest"])
            print "Warning : num of hotels = ", len(hotel_js["results"])
            print "Warning : num of flight = ", len(flight_js["results"])
    dest_score_list = sorted(dest_score_list, key=lambda score: score[0], reverse = True)
    return dest_score_list


# In[18]:

def formatRet(report):
    ret = {}
    ret["name"] = requestCodeToCity(report[1])
    routes = []
    for i in report[2]:
        curr = {}
        curr["flight"] = flight_dict[i[1]]
        curr["hotel"]  = hotel_dict[i[2]]
        curr["rating"] = i[0]
        routes.append(curr)
    ret["routes"] = routes
    ret["POIs"] = poi_dict[report[1]]["points_of_interest"]
    return ret
    
#ret = formatRet(dest_score_list[0])
#print ret


# In[19]:

def learnPOIList():
    # Precessing for just one time
    for city_name in support_name:
        if city_to_code_dict.has_key(city_name) == False:
            continue
        city_code = city_to_code_dict[city_name]
        poi_dict[city_code] = requestPoints(city_name)
        print city_code, " - ", city_name
        
        while (poi_dict[city_code].has_key("points_of_interest") == False or                len(poi_dict[city_code]["points_of_interest"]) == 0):
            print "Warning: no interest? dest = ", city_code
            print poi_dict[city_code]
            time.sleep(2)
            poi_dict[city_code] = requestPoints(requestCodeToCity(city_code))
    
    pickle.dump(poi_dict, open("/var/www/demo/poi_dict.pkl","wb"))


# In[20]:

def preprocessing():
    # BASIC API STAFF
    global apikey, sess, base
    apikey = "oz0gEI6TQenhtwNMnpI8UU7tYZfHvbAa"
    sess = requests.Session()
    base = "https://api.sandbox.amadeus.com/v1.2/"
    
    # CITY_TO_CODE_DICT
    global city_to_code_dict
    city_to_code_dict = {}
    with open('/var/www/demo/code.txt') as f:
        for l in f:
            curr = l.decode("utf-8").split()
            city_to_code_dict[" ".join(curr[:-2])] = curr[-2]
    f.close()
    
    # SUPPORT_DICT
    global support_name, support_code
    with open("/var/www/demo/cities.txt") as f:
        support_name = {x[:-1].decode("utf-8") for x in f}
        support_code = {x for x in map(lambda x : city_to_code_dict[x]                                   if city_to_code_dict.has_key(x) else x, support_name)}
    f.close()
    
    # FUNCTIONAL DICT
    global flight_dict, hotel_dict, poi_dict
    flight_dict, hotel_dict = {}, {}
    # learnPOIList()
    poi_dict = pickle.load(open("/var/www/demo/poi_dict.pkl","rb"))
    
    # XGB Model
    global xg, select_features
    xg = pickle.load(open("/var/www/demo/xg_model.pkl","rb"))
    select_features = ['average_rate', 'central_dst', 'flight_price', 'hotel_price', 'total_price', 'nonstop']


# In[21]:

# responseRequest API
def responseRequest(city_name, start_date, end_date, budget):
    # Error Check
    if city_to_code_dict.has_key(city_name) == False:
        return {"results" : [], "message" : "We are sorry that we don't support this city"}
    if datetime.strptime(start_date, "%Y-%m-%d") >= datetime.strptime(end_date, "%Y-%m-%d"):
        return {"results" : [], "message" : "Start date should be ealier than end date"}
    
    # Get messages
    origin = city_to_code_dict[city_name]
    print "origin = ", origin
    dest_score_list = getScoreList(origin, start_date, end_date, budget)
    ret = [formatRet(i) for i in dest_score_list]
    response = {"results" : ret[:3]}
    return response

#responseRequest("CHI", "2016-06-25", "2016-06-28", 1000)


# In[22]:

preprocessing()


# In[24]:

#t = responseRequest("Boston", "2016-06-25", "2016-06-28", 1000)
#t


# In[22]:

# responseRequest("Chicago", "2016-06-25", "2016-03-28", 1000)


# In[ ]:



