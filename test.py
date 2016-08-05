#!/usr/bin/python

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
<lang>de</lang>
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
    xml = '\n'.join([elem.text for elem in etree.fromstring(translation).iterfind('text')])
    print xml
    conn.close()


if __name__ == "__main__":
    main()
