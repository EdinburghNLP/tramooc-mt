from override_patterns import patterns

def override(sentences, translation_memory):
    forced_translation = {}

    for i, sentence in enumerate(sentences):
        # use translation memory for exact matches
        if translation_memory and sentence in translation_memory:
            forced_translation[i] = translation_memory[sentence]
            continue

        # copy sentences that match a Regex pattern
        for pattern in patterns:
            if pattern.search(sentence):
                forced_translation[i] = sentence.encode('UTF-8')
                break

    return forced_translation