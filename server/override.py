from override_patterns import patterns


def override(sentences):
    forced_translation = {}
    for i, sentence in enumerate(sentences):
        for pattern in patterns:
            if pattern.search(sentence):
                forced_translation[i] = sentence
                break

    return forced_translation