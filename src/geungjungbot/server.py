# -*- coding:utf-8 -*-

import logging as log
import sys
from flask import request, jsonify, Flask,  make_response
from flask_restful import Api

log.basicConfig(stream=sys.stdout, level=log.DEBUG)


app = Flask(__name__)
api = Api(app)

@api.representation('application/json')
@app.route('/keyboard', methods=['GET'])
def received_keyboard():
    log.info("Received keyboard")
    log.info(request.json)
    message = {
        "type": "text"
    }
    return make_response(jsonify(message), 200)

@api.representation('application/json')
@app.route('/message', methods=['POST'])
def received_message():
    log.info("Received Message")
    log.info(request.json)
    d = request.json
    log.info(d['content'].encode('utf-8'))
    message = {
        "message": {
            "text": d['content'].encode('utf-8')
        }
    }
    return make_response(jsonify(message), 200)

@api.representation('application/json')
@app.route('/friend', methods=['POST'])
def received_friend():
    log.info("Received Friend")
    log.info(request.json)
    message = {}
    return make_response(jsonify(message), 200)

@api.representation('application/json')
@app.route('/friend/<user_key>', methods=['DELETE'])
def received_friend_name(user_key):
    log.info("Received Friend %s" % user_key)
    log.info(request.json)
    message = {}
    return make_response(jsonify(message), 200)

@api.representation('application/json')
@app.route('/chat_room/<user_key>', methods=['DELETE'])
def received_chatroom_delete(user_key):
    log.info("Received Chatroom exit %s" % user_key)
    log.info(request.json)
    message = {}
    return make_response(jsonify(message), 200)

def spin(host='localhost', port=5000, debug=True):
    app.run(host=host, port=port, debug=debug)
