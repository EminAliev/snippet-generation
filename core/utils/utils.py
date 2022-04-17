import nltk
from nltk.corpus import stopwords

stop_words = stopwords.words('russian')
MIN_WORD_LENGTH = 4

nltk.download("stopwords")
nltk.download("wordnet")


def read_file(file_name):
    file = open(file_name, "r", encoding="utf-8")
    data = file.readlines()
    article = data[0].split(". ")
    sentences = []
    for sentence in article:
        sentences.append(sentence.replace("[^a-zA-Z]", " ").split(" "))
    sentences.pop()

    return sentences


def read_text(text):
    article = text.split(". ")
    sentences = []
    for sentence in article:
        sentences.append(sentence.replace("[^a-zA-Z]", " ").split(" "))
    sentences.pop()

    return sentences


def stop_word_process(word):
    if word in stop_words:
        return True
    if len(word) < MIN_WORD_LENGTH:
        return True
    return False
