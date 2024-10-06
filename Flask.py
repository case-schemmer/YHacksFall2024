import os
from flask import Flask, render_template, request
import requests
import json
app = Flask(__name__)

@app.route('/')
def student():
   return render_template('first.html')

# @app.route('/result',methods = ['POST', 'GET'])
# def result():
#    if request.method == 'POST':
#       result = request.form
#       return render_template("result.html",result = result)

@app.route('/data',methods = ['POST'])
def handle_get():
   tmp = os.popen("wolframscript -file thing.wls").read()
   result = request.form
   print(result)
   print(tmp)
   return render_template("result.html",result = tmp)

def cityToAddresses():
    headers = {
        'accept': 'application/json',
        'x-api-key': 'ybSJwuppzNOIWrOPUpw7QlRlGAWGhsG9'}
    params = {
        'text': '5201 California A',
        'countryCode': 'US'
    }

    response = requests.get('https://api.lightboxre.com/v1/addresses/_autocomplete', params=params, headers=headers)
    json_obj = json.loads(response.text)
    json_obj = json_obj["addresses"]
    addresses = []
    for i in json_obj:
        # subsub = i[i.index("wkt:"):]
        # sub = subsub[subsub[6:subsub.index("\'}")]]
        # addresses.append(sub)
        addresses.append((i["location"]["representativePoint"]["geometry"]["wkt"]))
    print(addresses)
    return addresses


def getAddressData(addresses):
    allScores = []
    for x in addresses:
        headers = {'accept': 'application/json','x-api-key': 'ybSJwuppzNOIWrOPUpw7QlRlGAWGhsG9'}
        params = {'wkt': x,'bufferDistance': '50','bufferUnit': 'm'}
        response = requests.get('https://api.lightboxre.com/v1/riskindexes/us/geometry', params=params, headers=headers)
        json_obj = json.loads(response.text)
        json_obj = json_obj["nris"]
        json_obj = str(json_obj[0])
        searches = ["socialVulnerability","communityResilience"]
        scores = []
        for i in searches:
            subsub = json_obj[json_obj.index(i):]
            sub = subsub[subsub.index("\'score\': "):]
            score = float(sub[9:sub.index(",")])
            scores.append(score)
        print(scores)
        allScores.append(scores)
    

    print(allScores)
if __name__ == '__main__':
   #app.run(debug = True, port=5001)
    addresses = cityToAddresses()
    getAddressData(addresses)
    with open('./data/positive.csv','wb') as myfile:
        wr = csv.writer(myfile) #, quoting=csv.QUOTE_ALL)
        wr.writerow(a)