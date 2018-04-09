import nltk
from nltk.corpus import wordnet, stopwords
from nltk.stem import WordNetLemmatizer
import string


class Preprocessor:
    def __init__(self):
        pass

    def get_wordnet_pos(self, treebank_tag):
        """
        return WORDNET POS compliance to WORDENT lemmatization (a,n,r,v)
        """
        if treebank_tag.startswith('J'):
            return wordnet.ADJ
        elif treebank_tag.startswith('V'):
            return wordnet.VERB
        elif treebank_tag.startswith('N'):
            return wordnet.NOUN
        elif treebank_tag.startswith('R'):
            return wordnet.ADV
        else:
            # As default pos in lemmatization is Noun
            return wordnet.NOUN

    def preprocess(self, text):
        # remove punctuations
        translate_table = dict((ord(char), ' ') for char in string.punctuation)
        text = text.translate(translate_table)

        # tokenize
        tokens = nltk.word_tokenize(text)

        # remove stopwords and translate all letter to lower case
        tokens = [word.lower() for word in tokens if word not in stopwords.words('english')]

        # get Part of Speech tags
        tags = nltk.pos_tag(tokens)

        # translate POS tags to wordnet tags
        wordnetTags = [(word, self.get_wordnet_pos(tag)) for word, tag in tags]

        # lemmatize
        lemmatizer = WordNetLemmatizer()
        lemmas = [lemmatizer.lemmatize(word, tag) for word, tag in wordnetTags]

        return lemmas


# if __name__ == "__main__":
#     p = Preprocessor()
#     result = p.preprocess(
#         "He's we're family-haha!"
#     )
#     print(result)

def processJson(text):
    p = Preprocessor()
    result = p.preprocess(text)
    return result