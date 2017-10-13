#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import atexit
import subprocess as sp
from time import sleep
import language_specific_settings

PREPROCESSOR = {}
POSTPROCESSOR = {}
TRANSLATOR = {}

CONFIG_TEMPLATE = """
beam-size: 5
normalize: yes
devices: {DEVICES}
workspace: 1024
models:
    - {MODEL_DIR}/model.npz
vocabs:
    - {MODEL_DIR}/vocab.{SRC}.json
    - {MODEL_DIR}/vocab.{TRG}.json
"""

def init(model_path, models, loglevel='error', port=50000):
    global PREPROCESSOR
    for model in models:
        server_dir = os.path.dirname(os.path.realpath(__file__))
        model_dir = "{}/{}".format(model_path, model)
        src = model.split('-')[0]
        trg = model.split('-')[1]
        tok_settings = '-l {}'.format(src)
        if model in language_specific_settings.input_tokenizer:
            tok_settings = language_specific_settings.input_tokenizer[model]
        command = "{}/preprocessor_server.py {} {} {} \"{}\" {}".format(server_dir,
                                                              model_dir,
                                                              src,
                                                              trg,
                                                              tok_settings,
                                                              port)
        print >> sys.stderr, "Starting preprocessor:", command
        atexit.register(sp.Popen(command, shell=True).kill)
        PREPROCESSOR[model] = 'ws://localhost:{}/preprocess'.format(port)
        port += 1

    global POSTPROCESSOR
    for model in models:
        server_dir = os.path.dirname(os.path.realpath(__file__))
        model_dir = "{}/{}".format(model_path, model)
        trg = model.split('-')[1]
        command = "{}/postprocessor_server.py {} {} {}".format(server_dir,
                                                               model_dir,
                                                               trg,
                                                               port)
        print >> sys.stderr, "Starting postprocessor:", command
        atexit.register(sp.Popen(command, shell=True).kill)
        POSTPROCESSOR[model] = 'ws://localhost:{}/postprocess'.format(port)
        port += 1

    global TRANSLATOR
    for model in models:
        server_path = os.path.dirname(os.path.realpath(__file__))
        command = "{}/../marian/build/server -c {}/{}/config.yml -p {} --log-level {} --type nematus " \
                .format(server_path, model_path, model, port, loglevel)
        print >> sys.stderr, "Starting translator:", command
        atexit.register(sp.Popen(command, shell=True).kill)
        TRANSLATOR[model] = 'ws://localhost:{}/translate'.format(port)
        port += 1
    sleep(10)
