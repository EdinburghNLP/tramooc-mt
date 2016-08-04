#!/usr/bin/python

import sys
from websocket import create_connection

MESSAGE = """
<msg>
<text>This is a test</text>
<lang>de</lang>
</msg>
"""

def main():
    """ main """
    conn = create_connection('ws://localhost:8080/translate')
    conn.send(MESSAGE)
    print conn.recv()
    conn.close()


if __name__ == "__main__":
    main()
