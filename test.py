#!/usr/bin/python

import sys
from websocket import create_connection
from lxml import etree


MESSAGE = """
<msg>
<text>This is a test.\nThis is another one.</text>
<lang>de</lang>
<domain>informal</domain>
</msg>
"""

def main():
    """ main """
    conn = create_connection('ws://localhost:8080/translate')
    conn.send(MESSAGE)

    translation = conn.recv()
    xml = etree.fromstring(translation).find('text').text
    print xml
    conn.close()


if __name__ == "__main__":
    main()
