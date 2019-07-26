#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from geungjungbot import GeungjungServer as Server



if __name__ == '__main__':

    config_file = os.environ.get('GEUNGJUNG_CONFIG', None)
    os.environ['PYTHONIOENCODING'] = 'UTF-8'

    Server.spin(config_file, host='localhost', port=5353, debug=True)
