#!/usr/bin/env python
#-*- coding:utf-8 -*-

import json
import logging as log
from flask import request, jsonify, Flask, json, make_response
from flask_restful import Api

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


if __name__ == '__main__':
    app.run(host='localhost', port=5353, debug=True)
