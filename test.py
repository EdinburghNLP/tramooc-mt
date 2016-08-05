#!/usr/bin/python

import sys
from websocket import create_connection
from lxml import etree


MESSAGE = """
<msg>
<lang>de</lang>
<domain>informal</domain>
<text>This is a test.</text>
<text>This is another one.</text>
</msg>
"""

def main():
    """ main """
    conn = create_connection('ws://localhost:8080/translate')
    conn.send(MESSAGE)

    translation = conn.recv()
    xml = '\n'.join([elem.text for elem in etree.fromstring(translation).iterfind('text')])
    print xml
    conn.close()


if __name__ == "__main__":
    main()
