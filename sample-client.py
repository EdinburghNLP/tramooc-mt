#!/usr/bin/python
# -*- coding: utf-8 -*-
# simple sample client with hard-coded XML input (for en-de)
# usage: python sample-client.py

from __future__ import unicode_literals, print_function
import sys
from websocket import create_connection
from lxml import etree

# we can optionally provide engine with translation memory
# for exact matches, translation memory will be used instead of MT engine
TRANSLATION_MEMORY = """
<tmx version="1.4">
  <header
    creationtool="XYZTool" creationtoolversion="1.01-023"
    datatype="PlainText" segtype="sentence"
    adminlang="en-us" srclang="en"
    o-tmf="ABCTransMem"/>
  <body>
    <tu>
      <tuv xml:lang="en">
        <seg>Hello world!</seg>
      </tuv>
      <tuv xml:lang="de">
        <seg>Hallo Welt! (using translation memory)</seg>
      </tuv>
    </tu>
  </body>
</tmx>
"""

MESSAGE = """
<msg>
<lang-source>en</lang-source>
<lang-target>de</lang-target>
<domain>informal</domain>
<text>This is a test.</text>
<text>This is another one.</text>
<text>This is an URL: http://please.com/do/no/translate/me</text>
<text>Hello world!</text>
{0}
</msg>
""".format(TRANSLATION_MEMORY)

def main():
    """ main """
    conn = create_connection('ws://localhost:8080/translate')
    conn.send(MESSAGE)

    translation = conn.recv()
    try:
        for elem in etree.fromstring(translation).iterfind('text'):
            print(elem.text.encode('UTF-8'))
    except Exception as e:
        sys.stderr.write(translation + '\n')
        raise
    conn.close()


if __name__ == "__main__":
    main()
