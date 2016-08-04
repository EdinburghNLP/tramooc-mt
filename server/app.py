#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import connexion
import settings
from bottle import request, Bottle, abort
from websocket import create_connection
from lxml import etree

model_path_prefix = sys.argv[1]
models = sys.argv[2:]

PORT = 8080

app = Bottle()


def translate(sentences, model):
    input_text = '\n'.join(sentences)
    translator = create_connection(settings.TRANSLATOR[model])
    translator.send(input_text)
    translated = translator.recv().strip().split('\n')
    translator.close()
    return translated


def preprocess(sentences, model):
    input_text = '\n'.join(sentences)
    preprocessor = create_connection(settings.PREPROCESSOR[model])
    preprocessor.send(input_text)
    preprocessed = preprocessor.recv().strip().split('\n')
    preprocessor.close()
    return preprocessed


def postprocess(sentences, model):
    input_text = '\n'.join(sentences)
    postprocessor = create_connection(settings.POSTPROCESSOR[model])
    postprocessor.send(input_text)
    postprocessed = postprocessor.recv().strip().split('\n')
    postprocessor.close()
    return postprocessed


def process_sentences(sentences, model):
    preprocessed = preprocess(sentences, model)
    translated = translate(preprocessed, model)
    post = postprocess(translated, model)
    return [sentence for sentence in post if sentence]


def parse_xml(message):
    xm = etree.fromstring(message)
    trg = xm.iterfind('lang').next().text
    model = 'en-{}'.format(trg)
    sentences = [sen.text.strip() for sen in xm.iterfind('text')]
    return model, sentences


def pack_into_xml(sentences, model):
    out = etree.Element('msg')
    src = model.split('-')[0]
    trg = model.split('-')[1]
    for sentence in sentences:
        child = etree.SubElement(out, 'text')
        child.text = sentence.strip()
        child.set('src', src)
        child.set('trg', trg)
    return etree.tostring(out)


@app.route('/translate')
def handle_websocket():
        wsock = request.environ.get('wsgi.websocket')
        if not wsock:
            abort(400, 'Expected WebSocket request.')

        while True:
            try:
                message = wsock.receive()
                if message is not None:
                    model, sentences = parse_xml(message)
                    trans = process_sentences(sentences, model)
                    wsock.send(pack_into_xml(trans, model))
            except WebSocketError:
                break


if __name__ == "__main__":
    settings.init(model_path_prefix, models)
    from gevent.pywsgi import WSGIServer
    from geventwebsocket import WebSocketError
    from geventwebsocket.handler import WebSocketHandler
    server = WSGIServer(("0.0.0.0", PORT), app,
                        handler_class=WebSocketHandler)
    print >> sys.stderr, "Running server on", PORT
    server.serve_forever()
