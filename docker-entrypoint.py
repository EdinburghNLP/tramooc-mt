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
        print >> sys.stderr, "Running amuNMT: ", command
        sp.call(command, shell=True)


def download_model(model):
    workdir = "{}/{}".format(MODEL_DIR, model)
    download_models.download_model(model, workdir)


def main():
    """ main """
    models = (' '.join(sys.argv[1:])).split(' ')
    print >> sys.stderr, "MODELS:", models
    for model in models:
        download_model(model)
    run_amunmt(models)


if __name__ == "__main__":
    main()
