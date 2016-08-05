# author: Rico Sennrich
# the MT engine will bypass sentences containing one of the patterns below,
# and instead copy them as-is from source to target
# this is useful for URLs and other technical terms,
# which would otherwise be destroyed from tokenization/translation

import re

regex_strings = set()

#URL
regex_strings.add('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')


patterns = []
for pattern in regex_strings:
    patterns.append(re.compile(pattern))