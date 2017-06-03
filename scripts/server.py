#!/usr/bin/env python

import os
from geungjungbot import GeungjungServer as Server


if __name__ == '__main__':

    config_file = os.environ['GEUNGJUNG_CONFIG']

    Server.spin(config_file, host='localhost', port=5353, debug=True)
