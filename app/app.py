from datetime import timedelta
from flask import Flask, make_response, request, current_app, jsonify
from functools import update_wrapper

import scratchclient
import requests
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
    false = False
    true = True
   
    try:
        scratchclient.ScratchSession(args.get('u'), args.get('p'))
        res['status'] = true
    except scratchclient.ScratchExceptions.InvalidCredentialsException:
        res['status'] = false
        
    res = jsonify(res)
    res.headers.add('Access-Control-Allow-Origin', '*')
    return res
    
