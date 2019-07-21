# -*- coding: utf-8 -*-

import os
from flask import Blueprint, jsonify, make_response, request
import traceback
from werkzeug.exceptions import Unauthorized

from ..models.user import get_user, User
from ..logger import logger
from ..utils import build_response
from ..run import db

mod = Blueprint('gb', __name__)

AUTH = os.environ['GEUNGJUNG_AUTH']


@mod.before_request
def authentication():
    headers = request.headers
    auth = headers.get("X-Api-Key")

    if auth != AUTH:
        raise Unauthorized


@mod.route('/fail', methods=['POST'])
def failure():
    message = 'failure'
    response = build_response(message)
    logger.info(response)
    return make_response(jsonify(response), 200)


@mod.route('/keyboard', methods=['GET'])
def received_keyboard():
    logger.info('Received keyboard')
    logger.info(request.json)
    message = {'type': 'text'}
    return make_response(jsonify(message), 200)


@mod.route('/message', methods=['POST'])
def received_message():
    logger.info("Received Message")
    logger.info(request.json)

    try:
        message = 'hihi'
    except Exception as e:
        logger.error(e)
        traceback.print_exc(file=logger.error)
        message = 'error..%s' % e

    response = build_response(message)
    logger.info(response)

    return make_response(jsonify(response), 200)


def parse_command(r):
    utterance = r['userRequest']['utterance']
    logger.info('Utterance: {}'.format(utterance.encode('utf-8')))
    try:
        command, param = utterance.encode('utf-8').split(',')
        logger.info(command)
        logger.info(param)
    except:
        command = None
        param = None
    return command, param


@mod.route('/entry', methods=['POST'])
def entry():
    """
    Check if authorized
       if yes, check if name is registered
    If not, ask for secret code
       if authorized:

    """


@mod.route('/fallback', methods=['POST'])
def fallback_message():
    logger.info("Received Message")
    logger.info(request.json)
    user = get_user(request.json)
    command, param = parse_command(request.json)

    if not command:
        if user:
            message = '안녕 {}'.format(user.name)
        else:
            message = '이름을 등록해줘'
    else:
        if user:
            message = '이미 {}로 등록됬어'.format(user.name)
        else:
            if command == '등록':
                u = User(request.json['userRequest']['user']['id'], param)
                db.session.add(u)
                db.session.commit()
                message = '이름이 {}로 등록되었어'.format(u.name)
            else:
                message = '모르는 명령어야. {}, {}'.format(command, param)
    response = build_response(message)
    logger.info(response)
    return make_response(jsonify(response), 200)
