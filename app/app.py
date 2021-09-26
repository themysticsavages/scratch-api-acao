from datetime import timedelta
from flask import Flask, make_response, request, current_app, jsonify
from functools import update_wrapper

import scratchclient
import requests
import base64
import json

#         The Scratch API
#        but CORS-friendly
#    and a bit incomplete lol

app = Flask(__name__)

# endpoints
@app.route('/')
def home():
    return { 'status': 'ok', 'more_at': 'https://scratchhh.tk' }

@app.route('/users/<user>/')
def user(user):
    res = jsonify(json.loads(requests.get('https://api.scratch.mit.edu/users/'+user).text))
    res.headers.add('Access-Control-Allow-Origin', '*')
    return res

@app.route('/projects/<id>/')
def project(id):
    res = jsonify(json.loads(requests.get('https://api.scratch.mit.edu/projects/'+id).text))
    res.headers.add('Access-Control-Allow-Origin', '*')
    return res

@app.route('/featured/')
def featured():
    res = jsonify(json.loads(requests.get('https://api.scratch.mit.edu/proxy/featured').text))
    res.headers.add('Access-Control-Allow-Origin', '*')
    return res

@app.route('/correctcredits/')
def checkuser():
    res = {'status':'pending'}
    args = request.args

    try:
      scratchclient.ScratchSession(args.get('user'), args.get('pass'))
      res['status'] = 'True'
    except scratchclient.ScratchExceptions.InvalidCredentialsException:
      res['status'] = 'False'
    
    res = jsonify(res)
    res.headers.add('Access-Control-Allow-Origin', '*')
    return res

@app.get('/api/fetchbackpack/')
def fetchback():
    args = request.args
    def get_user_backpack():
            user = base64.b64decode(args.get('user').encode('ascii')).decode('ascii')
            passwd = base64.b64decode(args.get('pass').encode('ascii')).decode('ascii')
        
            sess = scratchclient.ScratchSession(user, passwd)
            headers = {
                  "x-csrftoken": sess.csrf_token,
                  "X-Token": sess.token,
                  "x-requested-with": "XMLHttpRequest",
                  "Cookie": "scratchcsrftoken="
                  + sess.csrf_token
                  + ";scratchlanguage=en;scratchsessionsid="
                  + sess.session_id
                  + ";",
                  "referer": "https://scratch.mit.edu/users/" + user + "/",
            }
            req = requests.get('https://backpack.scratch.mit.edu/'+user+'/', headers=headers)
            return req.text
    userb = json.loads(get_user_backpack())

    content = []
    for cnt in userb:
            content.append(cnt['body'])
    res = jsonify(eval(str(content)))
    res.headers.add('Access-Control-Allow-Origin', '*')
    print(res.headers)
    return res
    
