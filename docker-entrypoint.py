#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess as sp

MODEL_DIR = "model"

print os.path.dirname(os.path.realpath(__file__))
COMMON_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append("{}/server".format(COMMON_DIR))
import download_models


def run_amunmt(models):
    while True:
        command = ' '.join(
            ['python', '{}/server/app.py'.format(COMMON_DIR),
             '{} {}'.format(MODEL_DIR, ' '.join(models))])
        print >> sys.stderr, "Running MarianNMT: ", command
        sp.call(command, shell=True)


def download_model(model, devices=[0]):
    workdir = "{}/{}".format(MODEL_DIR, model)
    download_models.download_model(model, workdir, devices=devices)


def main():
    """ main """
    models = {}
    for arg in sys.argv[1:]:
        args = arg.split(':')
        gpus = [0] if len(args) == 1 else [int(d) for d in args[1].split(',')]
        models[args[0]] = gpus
    print >> sys.stderr, "MODELS:", models
    for model, devices in models.iteritems():
        download_model(model, devices)
    run_amunmt(models.keys())


if __name__ == "__main__":
    main()
