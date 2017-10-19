#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess as sp
import argparse

MODEL_DIR = "model"

print os.path.dirname(os.path.realpath(__file__))
COMMON_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append("{}/server".format(COMMON_DIR))

import download_models


def run_amunmt(model_dir, models, subproc_port, loglevel):
    while True:
        command = ' '.join(
            ['python', '{}/server/app.py'.format(COMMON_DIR),
              model_dir,
              str(subproc_port),
              loglevel,
              ' '.join(models)])
        print >> sys.stderr, "Running MarianNMT: ", command
        sp.call(command, shell=True)

def main():
    """ main """
    args = parse_user_args()
    print >> sys.stderr, "MODELS:", args.models
    for model, devices in args.models.iteritems():
        download_models.download_model(model,
                                       os.path.join(args.model_dir, model),
                                       force=False,
                                       devices=devices)
    run_amunmt(args.model_dir,
               args.models.keys(),
               args.subproc_port,
               args.log_level)

def parse_user_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('model', nargs='+',
        help="models and GPUs, e.g. en-de:0,1 en-pl:1")
    parser.add_argument('--subproc-port', type=int, metavar='NUM', default=50000,
        help="ports for subprocessors, ports NUM...NUM+3 will be used")
    parser.add_argument('--model-dir', default='model', metavar='DIR',
        help="model directory, default: %(default)s")
    parser.add_argument('--verbose', action='store_true', help="print more logs")

    args = parser.parse_args()

    args.model_dir = os.path.abspath(args.model_dir)

    args.log_level = 'error'
    if args.verbose:
        args.log_level = 'info'

    args.models = {}
    for lang in args.model:
        fields = lang.split(':')
        gpus = [0] if len(fields) == 1 else [int(d) for d in fields[1].split(',')]
        args.models[fields[0]] = gpus
    return args


if __name__ == "__main__":
    main()
