#!/usr/bin/python

import sys
from websocket import create_connection


def main():
    """ main """
    conn = create_connection('ws://localhost:8080/translate')
    conn.send("This is a little test.\nThis is another one.")
    print conn.recv()
    conn.close()


if __name__ == "__main__":
    main()
