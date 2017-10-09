#!/usr/bin/python
# simple sample client that reads from stdin and write to stdout
# input is assumed to be UTF-8 plain text, untokenized, one sentence per line
# usage:
# python sample-client-2.py target_language < input_text > output_text

from __future__ import unicode_literals, print_function
import sys
from websocket import create_connection
from lxml import etree

output_language = sys.argv[1]

to_translate = []
for line in sys.stdin:
    elem = etree.Element('text')
    elem.text = line.strip().decode('UTF-8')
    to_translate.append(etree.tostring(elem))

MESSAGE = """
<msg>
<lang-source>en</lang-source>
<lang-target>{0}</lang-target>
<domain>informal</domain>
{1}
</msg>
""".format(output_language, '\n'.join(to_translate))

def main():
    """ main """
    conn = create_connection('ws://localhost:8080/translate')
    conn.send(MESSAGE)

    translation = conn.recv()
    try:
        for elem in etree.fromstring(translation).iterfind('text'):
            if elem.text is None:
              print('')
            else:
              print(elem.text.encode('UTF-8'))
    except Exception as e:
        sys.stderr.write(translation + '\n')
        raise
    conn.close()


if __name__ == "__main__":
    main()
