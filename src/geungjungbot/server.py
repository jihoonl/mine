# -*- coding:utf-8 -*-

from random import randint
import traceback
import yaml
import logging as log
import sys
from flask import request, jsonify, Flask,  make_response
from flask_restful import Api

log.basicConfig(stream=sys.stdout, level=log.DEBUG)

app = Flask(__name__)
api = Api(app)

MODE = {
    'repeat': True
}

config = None


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

    content = request.json['content'].encode('utf-8')

    try:
        if content == '칭찬해줘' or content == '칭찬':
            idx = randint(0, len(config) - 1)
            message = config[idx]
        elif content == '나를 따라해':
            if not MODE['repeat']:
                MODE['repeat'] = True
                message = '응 따라할게'
        elif content == '나를 그만 따라해':
            if MODE['repeat']:
                MODE['repeat'] = False
                message = '응 그만 따라할게'
        elif content == '모드':
            message = '나를 따라해, 나를 그만 따라해'
        else:
            if MODE['repeat']:
                message = content
            else:
                message = '잠깐만...'
    except Exception as e:
        log.error(e)
        traceback.print_exc(file=sys.stdout)
        message = '에러났어.. %s' % e

    response = {
        "message": {
            "text": message
        }
    }
    return make_response(jsonify(response), 200)


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


def _load_config(config_file):
    with open(config_file) as f:
        c = yaml.load(f)
    log.info(c)
    return c['cheerup']


def spin(config_file, host='localhost', port=5000, debug=True):
    global config
    config = _load_config(config_file)
    app.run(host=host, port=port, debug=debug)
