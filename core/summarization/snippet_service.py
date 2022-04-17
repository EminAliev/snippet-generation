from nltk.cluster.util import cosine_distance
from core.utils.utils import read_file, stop_word_process, read_text
import numpy as np
import networkx as nx


class SnippetGeneration:

    def sentence_similarity(self, one_word, two_word):
        one_word = [one.lower() for one in one_word]
        two_word = [two.lower() for two in two_word]

        words = list(set(one_word + two_word))

        first_vector = [0] * len(words)
        second_vector = [0] * len(words)

        for one in one_word:
            if stop_word_process(one):
                continue
            first_vector[words.index(one)] += 1

        for two in two_word:
            if stop_word_process(two):
                continue
            second_vector[words.index(two)] += 1

        return 0 if np.isnan(cosine_distance(first_vector, second_vector)) else 1 - cosine_distance(first_vector,
                                                                                                    second_vector)

    def build_similarity_matrix(self, sentences):
        matrix = np.zeros((len(sentences), len(sentences)))

        for x1 in range(len(sentences)):
            for x2 in range(len(sentences)):
                if x1 == x2:
                    continue
                matrix[x1][x2] = self.sentence_similarity(sentences[x1], sentences[x2])

        return matrix

    def generate_snippet(self, text=None, file_name=None, top_n=2):
        snippet = []
        if file_name:
            sentences = read_file(file_name)
        else:
            sentences = read_text(text)

        sentence_similarity_martix = self.build_similarity_matrix(sentences)

        sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_martix)
        scores = nx.pagerank(sentence_similarity_graph, max_iter=1000)

        ranked_sentence = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)

        for i in range(top_n):
            snippet.append(" ".join(ranked_sentence[i][1]))

        return ". ".join(snippet)
