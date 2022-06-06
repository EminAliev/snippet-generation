import nltk
from nltk import sent_tokenize, RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.snowball import RussianStemmer

from core.sentiments.sentiment_service import SentimentService

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
    sentiment_service = SentimentService()
    score = sentiment_service.predict(text)
    print(score)
    article = text.split(". ")
    sentences = []
    for sentence in article:
        sentences.append(sentence.replace("[^a-zA-Z]", " ").split(" "))
    sentences.pop()

    return sentences, score

def tokenize_stemmer_process(text):
    sentences = sent_tokenize(text)
    tokenizer = RegexpTokenizer(r'\w+')
    lmtzr = RussianStemmer()
    words = [set(lmtzr.stem(word) for word in tokenizer.tokenize(sentence.lower()))
             for sentence in sentences]
    return words


def stop_word_process(word):
    if word in stop_words:
        return True
    if len(word) < MIN_WORD_LENGTH:
        return True
    return False
