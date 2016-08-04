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

TOK_COMMAND = '{}/tokenizer/tokenizer.perl -l {} '.format(SCRIPT_PATH, LANG)
TRUE_COMMAND = '{}/recaser/truecase.perl --model {}'.format(SCRIPT_PATH,
                                                            TRUE_MODEL)

TOKENIZER = pexpect.spawn(TOK_COMMAND)
TOKENIZER.expect("Number of threads: .*\n")
TRUECASER = pexpect.spawn(TRUE_COMMAND)


def process_by_pipe(processor, sentences):
    processor.sendline('\n'.join(sentences))
    for i in range(len(sentences)):
        processor.readline()
    return [processor.readline().strip() for i in range(len(sentences))]


@sockets.route('/preprocess')
def preprocess(ws):
    while not ws.closed:
        message = ws.receive()

        if message:
            inList = message.split("\n")
            global TOKENIZER, TRUCASER
            preprocessed = process_by_pipe(TOKENIZER, inList)
            preprocessed = process_by_pipe(TRUECASER, preprocessed)
            ws.send('\n'.join(preprocessed))

if __name__ == '__main__':
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    server = pywsgi.WSGIServer(('', PORT), app,
                               handler_class=WebSocketHandler)
    print >> sys.stderr, "Preprocessing server for {} is running".format(LANG)
    server.serve_forever()
