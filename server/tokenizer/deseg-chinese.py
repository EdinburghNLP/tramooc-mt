#!/usr/bin/env python

from __future__ import print_function, unicode_literals
import re
import sys
import io
import codecs

# python 2/3 compatibility
if sys.version_info < (3, 0):
    sys.stderr = codecs.getwriter('UTF-8')(sys.stderr)
    sys.stdout = codecs.getwriter('UTF-8')(sys.stdout)
    sys.stdin = codecs.getreader('UTF-8')(sys.stdin)
else:
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', write_through=True, line_buffering=True)


re_space = re.compile(r"(?<![a-zA-Z])\s(?![a-zA-Z])", flags=re.UNICODE)
re_final_comma = re.compile("\.$")

for line in sys.stdin:
  line = line[:-1]
  line = re_space.sub("", line)
  line = line.replace(",", "\uFF0C")
  line = re_final_comma.sub("\u3002", line)
  sys.stdout.write(line + '\n')
