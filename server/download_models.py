#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import argparse
import sys
import os
import requests
from clint.textui import progress
from settings import CONFIG_TEMPLATE
import json
import subprocess

BASE_URL = "http://data.statmt.org/tramooc/prototype_v3/{}-{}/{}"
USER = "tramooc"
PASSWORD = "mooc4life"

def download_with_progress(path, url):
    r = requests.get(url, stream=True, auth=requests.auth.HTTPBasicAuth(USER, PASSWORD))
    with open(path, 'wb') as f:
        total_length = int(r.headers.get('content-length'))
        for chunk in progress.bar(r.iter_content(chunk_size=(1024 ** 2)),
                                  expected_size=(total_length/(1024 ** 2)) + 1):
            if chunk:
                f.write(chunk)
                f.flush()


def parse_args():
    """ parse command arguments """
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", dest="workdir", default='.')
    parser.add_argument('-m', dest="model", default='en-de')
    parser.add_argument('-f', dest="force", default=False)
    return parser.parse_args()


def make_workdir(path):
    """ Create a directory. """
    workdir = os.path.abspath(path)

    try:
        os.makedirs(workdir)
    except OSError:
        pass


def download_model(model, workdir, mariandir, force=False, devices=[0]):
    """ download Rico Sennrich's WMT16 model: <src> to <trg>. """
    make_workdir(workdir)
    download_model_parts(model, workdir, mariandir, force)
    create_base_config(model, workdir, devices)


def download_model_parts(model, workdir, mariandir, force=False):
    src = model.split('-')[0]
    trg = model.split('-')[1]

    model_parts = ["model.npz",
                   "model.npz.json",
                   "vocab.{}.json".format(src),
                   "vocab.{}.json".format(trg),
                   "{}{}.bpe".format(src, trg),
                   "{}.vocab".format(src),
                   "truecase-model.{}".format(src)]

    for part in model_parts:
        download_file(src, trg, part, workdir, force)
    inject_s2s_config(os.path.join(workdir, 'model.npz'), mariandir)


def download_file(src, trg, name, workdir, force=False):
    path = os.path.join(workdir, name)
    if not os.path.exists(path):
        full_url = BASE_URL.format(src, trg, name)
        print >> sys.stderr, "Downloading: {} to {}".format(full_url, path)
        download_with_progress(path, full_url)
    elif force:
        full_url = BASE_URL.format(src, trg, name)
        print >> sys.stderr, "Force downloading: {}".format(full_url)
        download_with_progress(path, full_url)
    else:
        print >> sys.stderr, "File {} exists. Skipped".format(path)


def inject_s2s_config(model_path, marian_path='./marian'):
    print >> sys.stderr, "Adding s2s parameters into {}".format(model_path)
    script = os.path.join(marian_path, 'src/marian/scripts/contrib/inject_s2s_config.py')
    command = "python {s} --json {p}.json --model {p}".format(s=script, p=model_path)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    process.wait()


def create_base_config(model, model_dir, devices=[0]):
    src = model.split('-')[0]
    trg = model.split('-')[1]
    gpu_list = "[{}]".format(",".join(str(d) for d in devices))
    config = CONFIG_TEMPLATE.format(DEVICES=gpu_list,
                                    SRC=src,
                                    TRG=trg,
                                    MODEL_DIR=model_dir)
    with open("{}/config.yml".format(model_dir), 'w') as config_file:
        config_file.write(config)


def main():
    """ main """
    args = parse_args()

    print >> sys.stderr,  "Downloading {} to {}".format(args.model,
                                                        args.workdir)
    download_model(args.model, args.workdir, args.force)


if __name__ == "__main__":
    main()
