from nltk.corpus import wordnet


def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word, lang='spa'):
        for lemma in syn.lemmas("spa"):
            synonyms.add(lemma.name())
    return list(synonyms)