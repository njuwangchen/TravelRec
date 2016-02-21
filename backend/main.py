import json
from flask import Flask, request
# from hack import responseRequest
from hack import responseRequest
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def hello():
    print request.json
    origin = request.json['from']
    depart = request.json['depart'].split('T')[0]
    return_ = request.json['return'].split('T')[0]
    budget = int(request.json['budget'])
    res = responseRequest(origin, depart, return_, budget)
    return json.dumps(res)

if __name__ == "__main__":
    app.run()
