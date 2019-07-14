# -*- coding:utf-8 -*-

import ast
from itertools import cycle
import traceback
import yaml
import logging as log
import sys
from flask import request, jsonify, Flask,  make_response
from flask_restful import Api
import json

# My custom module
import utils

log.basicConfig(stream=sys.stdout, level=log.DEBUG)

app = Flask(__name__)
api = Api(app)

MODE = {
    'repeat': True,
    'reverse': True
}

config = None


def _build_response(message):
    # message contains only string data.
    if isinstance(message, unicode):
        response = {
            "message": {
                "text": message.encode('utf-8')
            }
        }
    elif isinstance(message, str):
        response = {
            "message": {
                "text": message
            }
        }
    elif isinstance(message, dict):
        response = {
            "message": {
                "text": message['text'].encode('utf-8'),
                "photo": {
                    "url": message['photo'].encode('utf-8'),
                    "width": 640,
                    "height": 480
                }
            }
        }
    else:
        response = {
            "message": {
                "text": "에러났어. " + str(type(message))
            }
        }

    return response


@api.representation('application/json')
@app.route('/keyboard', methods=['GET'])
def received_keyboard():
    log.info("Received keyboard")
    log.info(request.json)
    message = {
        "type": "text"
    }
    return make_response(jsonify(message), 200)


# @api.representation('application/json')
@app.route('/message', methods=['POST'])
def received_message():
    log.info("Received Message")
    try:
        log.info(request)
        data = request.get_json(force=True)
        log.info(data)

        raw_content = data['content']
        content = raw_content.encode('utf-8')

        selected = False
        for k, v in config.items():
            if any(keyword.encode('utf-8') in content for keyword in v['key']):
                message = v['reply'].next()
                selected = True
        if selected:
            pass
        elif '힘들어' in content:
            message = '힘내! 내가 있자나' + utils.get_heart(2)
        elif content == '너 멋있어':
            message = '나도 알아'
        elif content == '사랑해':
            message = '나도 사랑해' + utils.get_heart(2)
        elif content == '따라해':
            if not MODE['repeat']:
                MODE['repeat'] = True
                message = '응'
            else:
                message = '이미 따라하고 있어'
        elif content == '그만 따라해':
            if MODE['repeat']:
                MODE['repeat'] = False
                message = '응'
            else:
                message = '뭐래..'
        elif content == '뒤집어':
            if not MODE['reverse']:
                MODE['reverse'] = True
                message = '응'
            else:
                message = '어있 고집뒤 미이'
        elif content == '그만 뒤집어':
            if MODE['reverse']:
                MODE['reverse'] = False
                message = '응'
            else:
                message = '뭐래..'
        elif content == '명령어':
            message = '따라해, 그만 따라해, 뒤집어, 그만 뒤집어'
        elif content == '현황':
            m = []
            for k, v in MODE.items():
                m.append('%s : %s' % (k, v))
            message = '\n'.join(m)
        else:
            if MODE['reverse']:
                message = raw_content[::-1].encode('utf-8')
            elif MODE['repeat']:
                message = content
            else:
                message = '훙항힝항홍항항히아하이항'
    except Exception as e:
        log.error(e)
        traceback.print_exc(file=sys.stdout)
        message = '에러났어.. %s' % e

    response = _build_response(message)
    log.info(response)

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

    for k in c.keys():
        c[k]['reply'] = cycle(c[k]['reply'])
    return c


def spin(config_file, host='localhost', port=5000, debug=True):
    global config
    config = _load_config(config_file)
    app.run(host=host, port=port, debug=debug)
