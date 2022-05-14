import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk import word_tokenize
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
import pickle
from collections import defaultdict

train_data = pd.read_json('data/train.json')
test_data = pd.read_json('data/test.json')


def ru_token(string):
    return [i.lower() for i in word_tokenize(string) if re.match(r'[\u0400-\u04ffа́]+$', i)]


sentiment_parameters = {}
sentiment_parameters['tokenizer'] = ru_token
sentiment_parameters['stop_words'] = stopwords.words('russian')
sentiment_parameters['ngram_range'] = (1, 3)
sentiment_parameters['min_df'] = 3

tf_idf = TfidfVectorizer(**sentiment_parameters)

# Задаем параметры для tf–idf

data = train_data.append(test_data, ignore_index=True)
tf_idf.fit([row['text'].lower() for index, row in data.iterrows()])

train_one, train_two, train_three = defaultdict(list), defaultdict(list), defaultdict(list)
for index, row in train_data.iterrows():
    train_three[row['sentiment']].append(row['text'].lower())
for element in train_three:
    train_one[element], train_two[element] = train_test_split(train_three[element], test_size=0.2, random_state=2022)


def align(some_dict):
    random_state = np.random.RandomState(2022)

    max_len = 0

    for key in some_dict:
        max_len = max(max_len, len(some_dict[key]))
    print('max_len: ' + str(max_len))

    tmp = defaultdict(list)
    for key in some_dict:
        if len(some_dict[key]) < max_len:

            _tmp = some_dict[key].copy()
            random_state.shuffle(_tmp)

            tmp[key] = some_dict[key] * (max_len // len(some_dict[key])) + _tmp[:(max_len % len(some_dict[key]))]
            random_state.shuffle(tmp[key])
        else:
            tmp[key] = some_dict[key]
    return tmp


train_one = align(train_one)

train_x = []
for i in sorted(train_one.keys()):
    for j in train_one[i]:
        train_x.append(j)

train_y = []
for i in sorted(train_one.keys()):
    for j in train_one[i]:
        train_y.append(i)

multinomial = MultinomialNB()
multinomial.fit(tf_idf.transform(train_x), train_y)

with open('model.pkl', 'wb+') as f:
    pickle.dump((tf_idf, multinomial), f)
