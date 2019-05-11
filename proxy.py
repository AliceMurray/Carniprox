import json
import dateutil
import dateutil.parser

from datetime import datetime
import time

from flask import Flask
from flask import jsonify
from flask import request

from http.client import HTTPSConnection, HTTPConnection
from base64 import b64encode


app = Flask(__name__)

DOMJUDGE_HOST = "contest.domjudge.org"
DOMJUDGE_API_PATH = "/api/"

def __visit_getresponse(url):

    c = HTTPSConnection(DOMJUDGE_HOST)
    userAndPass = b64encode("{}:{}".format(request.authorization.username, request.authorization.password).encode()).decode("ascii")
    headers = { 'Authorization' : 'Basic %s' %  userAndPass }

    if "cid" in request.args:
        url = "/".join(["contests", request.args["cid"], url])

    if "public" in request.args:
        url += "?public=true"

    url = DOMJUDGE_API_PATH + url
    #print("visit: " + url)

    #r = c.request('GET', '/demoweb')#url, headers=headers)
    c.request('GET', url, headers=headers)
    #time.sleep(2)
    r = c.getresponse()
    #print("response: " + str(r))
    #print(r.status)

    return r

def __to_json(response):
    answer = response.read().decode("ascii")
    #print(answer)
    answer = json.loads(answer)
    #print(answer)
    return answer

@app.route('/config')
def config():
    response = __visit_getresponse("config")
    answer = __to_json(response)
    return jsonify(answer)

def timespan_to_seconds(tim):
    relevant = tim.split('.')[0]
    h, m, s = map(int, relevant.split(":"))
    return h * 3600 + m * 60 + s

@app.route('/contests')
def contests():
    response = __visit_getresponse("contests")
    answer = __to_json(response)
    converted_ans = {}
    for a in answer:
        a["id"] = int(a["id"])
        a["start"] = int(dateutil.parser.parse(a["start_time"]).timestamp())
        a["end"] = int(dateutil.parser.parse(a["end_time"]).timestamp())
        a["freeze"] = a["end"] - timespan_to_seconds(a["scoreboard_freeze_duration"])
        a["penalty"] = int(a["penalty_time"]) * 60

        converted_ans[a["id"]] = a

    return jsonify(converted_ans)

@app.route('/categories')
def categores():
    response = __visit_getresponse("groups")
    answer = __to_json(response)
    converted_ans = []
    for a in answer:
        a["categoryId"] = int(a["id"])
        converted_ans.append(a)

    return jsonify(converted_ans)

@app.route('/teams')
def teams():
    #then connect
    #get the response back
    response = __visit_getresponse("teams")
    answer = __to_json(response)
    converted_ans = []
    for a in answer:
        a["id"] = int(a["id"])
        a["category"] = int(a["group_ids"][0])
        converted_ans.append(a)
    return jsonify(converted_ans)

@app.route('/submissions')
def submissions():
    response = __visit_getresponse("submissions")
    answer = __to_json(response)
    converted_ans = []
    for a in answer:
        a["id"] = int(a["id"])
        a["time"] = int(dateutil.parser.parse(a["time"]).timestamp())

        a["problem"] = int(a["problem_id"])
        a["team"] = int(a["team_id"])

        converted_ans.append(a)

    return jsonify(converted_ans)
#     return jsonify(a='Hello, World!')

@app.route('/problems')
def problems():
    response = __visit_getresponse("problems")
    answer = __to_json(response)
    converted_ans = []
    for a in answer:
        a["id"] = int(a["id"])
        converted_ans.append(a)

    return jsonify(converted_ans)

judge_answers = {
        "AC": "correct",
        "CE": "compiler-error",
        "WA" : "wrong answer",
        "MLE" : "memory limit",
        "TLE" : "timelimit",
        "PE" : "presentation error",
        "RTE" : "runtime error",
        "NO" : "no output",
}


@app.route('/judgings')
def judgings():
    response = __visit_getresponse("judgements")
    answer = __to_json(response)

    converted_ans = []
    for a in answer:
        a["id"] = int(a["id"])
        a['submission'] = int(a['submission_id'])
        if a['judgement_type_id'] not in judge_answers:
            continue
        a['outcome'] = judge_answers[a['judgement_type_id']]
        a["time"] = int(dateutil.parser.parse(a["start_time"]).timestamp())

        converted_ans.append(a)

    return jsonify(converted_ans)

if __name__ == "__main__":
    app.run()
