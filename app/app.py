from datetime import timedelta
from flask import Flask, make_response, request, current_app, jsonify
from functools import update_wrapper

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
    return res

@app.route('/projects/<id>/')
def project(id):
    res = jsonify(json.loads(requests.get('https://api.scratch.mit.edu/projects/'+id).text))
    return res

@app.route('/featured/')
def featured():
    res = jsonify(json.loads(requests.get('https://api.scratch.mit.edu/proxy/featured').text))
    return res
