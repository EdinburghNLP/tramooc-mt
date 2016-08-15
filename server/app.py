#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import connexion
import settings
from bottle import request, Bottle, abort
from websocket import create_connection
from lxml import etree
from override import override

model_path_prefix = sys.argv[1]
models = sys.argv[2:]

PORT = 8080

app = Bottle()

class EngineException(Exception):
    pass

def translate(sentences, model):
    input_text = '\n'.join(sentences)
    translator = create_connection(settings.TRANSLATOR[model])
    translator.send(input_text)
    translated = translator.recv().strip().split('\n')
    translator.close()
    return translated


def preprocess(sentences, model):
    input_text = '\n'.join(sentences)
    try:
        preprocessor = create_connection(settings.PREPROCESSOR[model])
    except KeyError:
        raise EngineException('Error: language pair {0} not found among running instances.'.format(model))
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

# validate input
# we currently disallow line breaks in input, since this is internally
# treated as sentence boundary
def validate(sentences):
    if any('\n' in sentence for sentence in sentences):
        raise EngineException('Error: input may not contain line breaks.')

def process_sentences(sentences, model, translation_memory):
    validate(sentences)
    forced_translations = override(sentences, translation_memory)
    preprocessed = preprocess(sentences, model)
    translated = translate(preprocessed, model)
    post = [sentence for sentence in postprocess(translated, model) if sentence]
    for i in forced_translations:
        post[i] = forced_translations[i]
    return post

def extract_tmx(tmx, src, trg):
    memory = {}
    body = tmx.find('body')
    for tu in body.iterfind('tu'):
        cur_src = None
        cur_trg = None
        for tuv in tu.iterfind('tuv'):
            lang = tuv.get('{http://www.w3.org/XML/1998/namespace}lang')
            if lang == src:
                cur_src = tuv.find('seg').text
            elif lang == trg:
                cur_trg = tuv.find('seg').text
        if cur_src and cur_trg:
            memory[cur_src] = cur_trg
    return memory

def parse_xml(message):
    xm = etree.fromstring(message)
    src = xm.iterfind('lang-source').next().text
    trg = xm.iterfind('lang-target').next().text
    model = '{}-{}'.format(src, trg)
    sentences = [sen.text.strip() for sen in xm.iterfind('text')]
    if xm.find('tmx'):
        tmx = extract_tmx(xm.find('tmx'), src, trg)
    else:
        tmx = None

    return model, sentences, tmx


def pack_into_xml(sentences, model):
    out = etree.Element('msg')
    src = model.split('-')[0]
    trg = model.split('-')[1]
    for sentence in sentences:
        child = etree.SubElement(out, 'text')
        child.text = sentence.decode("UTF-8")
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
                    model, sentences, translation_memory = parse_xml(message)
                    try:
                        trans = process_sentences(sentences, model, translation_memory)
                        wsock.send(pack_into_xml(trans, model))
                    except EngineException as e:
                        wsock.send(e)
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
