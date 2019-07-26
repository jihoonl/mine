# -*- coding: utf-8 -*-

import os
from flask import Blueprint, jsonify, make_response, request, redirect, url_for, render_template
import traceback
from werkzeug.exceptions import Unauthorized

from ..models.user import get_user, User
from ..models.cheers import get_types, get_message
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

def parse_command(utterance):
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
    pass


#@mod.route('/')
#def index():
#    datasets = User.query.all()
#    return render_template('index.html', users=datasets)


@mod.route('/<utterance>')
def add_user(utterance):
    logger.info('Add User')
    command, param = parse_command(utterance)
    if command == '등록':
        u = User(request.json['userRequest']['user']['id'], param)
        db.session.add(u)
        db.session.commit()
        message = '이름이 {}로 등록되었어'.format(u.name)
    else:
        message = '이름 먼저 등록해줘.'
    response = build_response(message)
    logger.info(response)
    return make_response(jsonify(response), 200)


@mod.route('/fallback', methods=['POST'])
def fallback_message():
    logger.info("Received Message")
    logger.info(request.json)
    user = get_user(request.json)
    utterance = request.json['userRequest']['utterance']

    logger.info('Utterance: {}'.format(utterance.encode('utf-8')))
    if not user:
        return add_user(utterance=utterance)
    utterance = utterance.encode('utf-8')

    command, param = parse_command(utterance)

    if '등록' in utterance:
        message = '이미 {}로 등록됬어'.format(user.name)
        response = build_response(message)
    else:
        types = get_types()

        m = None
        for t in types:
            if t in utterance:
                m = get_message(t)
                break
        if m:
            if isinstance(m, str):
                message = '{}아, {}'.format(user.name, m)
                response = build_response(message)
            elif isinstance(m, dict):
                response = build_response(m)
            elif isinstance(m, unicode):
                message = '{}아, {}'.format(user.name, m.encode('utf-8'))
                response = build_response(message)
            else:
                logger.info(type(m))
                message = '안녕 {}'.format(user.name)
                response = build_response(message)
        else:
            message = '안녕 {}'.format(user.name)
            response = build_response(message)
    logger.info(response)
    return make_response(jsonify(response), 200)
