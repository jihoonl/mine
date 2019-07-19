# -*- coding: utf-8 -*-

import os
from flask import Blueprint, jsonify, make_response, request
import traceback
from werkzeug.exceptions import Unauthorized

from ..logger import logger
from ..utils import build_response

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


@mod.route('/fallback', methods=['POST'])
def fallback_message():
    logger.info("Received Message")
    logger.info(request.json)
    message = '안녕 '
    response = build_response(message)
    logger.info(response)
    return make_response(jsonify(response), 200)
