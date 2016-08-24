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
TOK_SETTINGS = sys.argv[3]
TRUE_MODEL = "{}/truecase-model.{}".format(MODEL_PATH, LANG)
PORT = int(sys.argv[4])

NORM_COMMAND = '{}/tokenizer/normalize-punctuation.perl'.format(SCRIPT_PATH)
TOK_COMMAND = '{}/tokenizer/tokenizer.perl {} '.format(SCRIPT_PATH, TOK_SETTINGS)
TRUE_COMMAND = '{}/recaser/truecase.perl --model {}'.format(SCRIPT_PATH,
                                                            TRUE_MODEL)

NORMALIZER = pexpect.spawn(NORM_COMMAND)
TOKENIZER = pexpect.spawn(TOK_COMMAND)
TOKENIZER.expect("Number of threads: .*\n")
TRUECASER = pexpect.spawn(TRUE_COMMAND)


def process_by_pipe(processor, sentences, max_sentences=10):
    start = 0
    ret = []
    while start < len(sentences):
        processor.sendline('\n'.join(sentences[start:start+max_sentences]))
        for i in range(min(max_sentences, len(sentences)-start)):
            processor.readline()
        for i in range(min(max_sentences, len(sentences)-start)):
            ret.append(processor.readline().strip())
        start += max_sentences
    return ret


@sockets.route('/preprocess')
def preprocess(ws):
    while not ws.closed:
        message = ws.receive()

        if message:
            inList = message.split("\n")
            global NORMALIZER, TOKENIZER, TRUCASER
            preprocessed = process_by_pipe(NORMALIZER, inList)
            preprocessed = process_by_pipe(TOKENIZER, preprocessed)
            preprocessed = process_by_pipe(TRUECASER, preprocessed)
            ws.send('\n'.join(preprocessed))

if __name__ == '__main__':
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    server = pywsgi.WSGIServer(('', PORT), app,
                               handler_class=WebSocketHandler)
    print >> sys.stderr, "Preprocessing server for {} is running".format(LANG)
    server.serve_forever()
