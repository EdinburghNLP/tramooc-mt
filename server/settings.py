#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import atexit
import subprocess as sp
from time import sleep

PREPROCESSOR = {}
POSTPROCESSOR = {}
TRANSLATOR = {}


def init(model_path, models):
    port = 50000

    global PREPROCESSOR
    for model in models:
        server_dir = os.path.dirname(os.path.realpath(__file__))
        model_dir = "{}/{}".format(model_path, model)
        src = model.split('-')[0]
        command = "{}/preprocessor_server.py {} {} {}".format(server_dir,
                                                              model_dir,
                                                              src,
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
