#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import pexpect
from flask import Flask
from flask_sockets import Sockets

app = Flask(__name__)
sockets = Sockets(app)

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
MODEL_PATH = sys.argv[1]
LANG = sys.argv[2]
TRUE_MODEL = "{}/truecase-model.{}".format(MODEL_PATH, LANG)
PORT = int(sys.argv[3])

if LANG == 'zh':
    DETOK_COMMAND = 'python3 {}/tokenizer/deseg-chinese.py'.format(SCRIPT_PATH)
else:
    DETOK_COMMAND = '{}/tokenizer/detokenizer.perl -q -l {}'.format(SCRIPT_PATH,
                                                                LANG)

DETRUE_COMMAND = '{}/recaser/detruecase.perl'.format(SCRIPT_PATH)

DETOKENIZER = pexpect.spawn(DETOK_COMMAND)
DETRUECASER = pexpect.spawn(DETRUE_COMMAND)

DETOKENIZER.delaybeforesend = 0
DETRUECASER.delaybeforesend = 0

def process_by_pipe(processor, sentences):
    ret = []
    for sentence in sentences:
        processor.sendline(sentence)
        processor.readline()
        ret.append(processor.readline().strip())
    return ret


@sockets.route('/postprocess')
def postprocess(ws):
    while not ws.closed:
        message = ws.receive()

        if message:
            message = message.replace("@@ ", "") # merge BPE units
            inList = message.split("\n")
            global DETOKENIZER, DETRUCASER
            preprocessed = process_by_pipe(DETRUECASER, inList)
            preprocessed = process_by_pipe(DETOKENIZER, preprocessed)
            p = [sent.decode('UTF-8', 'replace') for sent in preprocessed]
            ws.send('\n'.join(p))

if __name__ == '__main__':
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    server = pywsgi.WSGIServer(('', PORT), app,
                               handler_class=WebSocketHandler)
    print >> sys.stderr, "Postrocessing server for {} is running".format(LANG)
    server.serve_forever()
