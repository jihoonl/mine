#!/usr/bin/env python

from geungjungbot import GeungjungServer as Server


if __name__ == '__main__':
    Server.spin(host='localhost', port=5353, debug=True)
