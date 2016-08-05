from override_patterns import patterns


def override(sentences, translation_memory):
    forced_translation = {}

    for i, sentence in enumerate(sentences):
        if translation_memory and sentence in translation_memory:
            forced_translation[i] = translation_memory[sentence]
            continue

        for pattern in patterns:
            if pattern.search(sentence):
                forced_translation[i] = sentence
                break

    return forced_translation