#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import atexit
import subprocess as sp
from time import sleep
import language_specific_settings

PREPROCESSOR = {}
POSTPROCESSOR = {}
TRANSLATOR = {}

CONFIG_TEMPLATE = """
# Paths are relative to config file location
relative-paths: yes

# performance settings
beam-size: 12
normalize: yes
threads: 8

# scorer configuration
scorers:
  F0:
    path: ./model.ens0.npz
    type: Nematus

  F1:
    path: ./model.ens1.npz
    type: Nematus

  F2:
    path: ./model.ens2.npz
    type: Nematus

  F3:
    path: ./model.ens3.npz
    type: Nematus

# scorer weights
weights:
  F0: 0.25
  F1: 0.25
  F2: 0.25
  F3: 0.25

bpe: ./{}{}.bpe

# vocabularies
source-vocab: ./vocab.{}.json
target-vocab: ./vocab.{}.json
"""

def init(model_path, models):
    port = 50000

    global PREPROCESSOR
    for model in models:
        server_dir = os.path.dirname(os.path.realpath(__file__))
        model_dir = "{}/{}".format(model_path, model)
        src = model.split('-')[0]
        tok_settings = '-l src'
        if model in language_specific_settings.input_tokenizer:
            tok_settings = language_specific_settings.input_tokenizer[model]
        command = "{}/preprocessor_server.py {} {} \"{}\" {}".format(server_dir,
                                                              model_dir,
                                                              src,
                                                              tok_settings,
                                                              port)
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
        atexit.register(sp.Popen(command, shell=True).kill)
        POSTPROCESSOR[model] = 'ws://localhost:{}/postprocess'.format(port)
        port += 1

    global TRANSLATOR
    for model in models:
        server_path = os.path.dirname(os.path.realpath(__file__))
        command = "{}/../amunmt/scripts/amunmt_server.py -c {}/{}/config.yml -p {}".format(server_path,
                                                                   model_path,
                                                                   model,
                                                                   port)
        atexit.register(sp.Popen(command, shell=True).kill)
        TRANSLATOR[model] = 'ws://localhost:{}/translate'.format(port)
        port += 1
    sleep(10)
