import io
import itertools
import os

import click
import networkx as nx
import nltk
import underthesea

import re

def word_tokenize_en(text):
    return nltk.word_tokenize(text)

def word_tokenize_vi(text):
    return underthesea.word_tokenize(text)

def pos_tag_en(wordTokens):
    return nltk.pos_tag(wordTokens)

def pos_tag_vi(text):
    tagged = []
    for sent in underthesea.sent_tokenize(text):
        tagged += underthesea.pos_tag(sent)
    return tagged

def filter_for_tags_en(tagged, tags=['NN', 'JJ', 'NNP']):
    # NN noun, singular ‘desk’
    # JJ adjective ‘big’
    # NNP proper noun, singular ‘Harrison’
    return [item for item in tagged if item[1] in tags]

def filter_for_tags_vi(tagged, tags=['N', 'A', 'Np', 'B' , 'Nb', 'NNP']):
    # N noun, singular ‘desk’
    # A adjective ‘big’
    # Np proper noun, singular ‘Harrison’
    # B từ mượn karaoke, nilông, fax, oxy
    # Nb tivi, két, casino, golf, bar
    # NNP VN, Nguyễn, Văn
    return [item for item in tagged if item[1] in tags]

def normalize(tagged):
    return [(item[0].replace('.', ''), item[1]) for item in tagged]


def unique_everseen(iterable, key=None):
    "List unique elements, preserving order. Remember all elements ever seen."
    # unique_everseen('AAAABBBCCDAABBB') --> A B C D
    # unique_everseen('ABBCcAD', str.lower) --> A B C D
    seen = set()
    seen_add = seen.add
    if key is None:
        for element in [x for x in iterable if x not in seen]:
            seen_add(element)
            yield element
    else:
        for element in iterable:
            k = key(element)
            if k not in seen:
                seen_add(k)
                yield element


def buildGraph(nodes):
    """nodes - list of hashables that represents the nodes of the graph"""
    gr = nx.Graph()  # initialize an undirected graph
    gr.add_nodes_from(nodes)
    nodePairs = list(itertools.combinations(nodes, 2))

    # add edges to the graph (weighted by Levenshtein distance)
    for pair in nodePairs:
        firstString = pair[0]
        secondString = pair[1]
        levDistance = lDistance(firstString, secondString)
        gr.add_edge(firstString, secondString, weight=levDistance)

    return gr


def pagerank(graph, weight='weight'): 
    return nx.pagerank(graph, weight='weight')

def lDistance(firstString, secondString):
    """Function to find the Levenshtein distance between two words/sentences -
    gotten from http://rosettacode.org/wiki/Levenshtein_distance#Python
    """
    if len(firstString) > len(secondString):
        firstString, secondString = secondString, firstString
    distances = range(len(firstString) + 1)
    for index2, char2 in enumerate(secondString):
        newDistances = [index2 + 1]
        for index1, char1 in enumerate(firstString):
            if char1 == char2:
                newDistances.append(distances[index1])
            else:
                newDistances.append(1 + min((distances[index1],
                                             distances[index1 + 1],
                                             newDistances[-1])))
        distances = newDistances
    return distances[-1]

def load_stop_words(stop_word_file):
    """
    Utility function to load stop words from a file and return as a list of words
    @param stop_word_file Path and file name of a file containing stop words.
    @return list A list of stop words.
    """
    stop_words = []
    for line in open(stop_word_file, 'r', encoding="utf-8"):
        if line.strip()[0:1] != "#":
            stop_words.append(line.rstrip())
    return stop_words

def build_stop_word_regex(stop_word_list):
    stop_word_regex_list = []
    for word in stop_word_list:
        word_regex = '\\b' + word + '\\b'
        stop_word_regex_list.append(word_regex)
    stop_word_pattern = re.compile('|'.join(stop_word_regex_list), re.IGNORECASE)
    return stop_word_pattern

def preprocess(text, stop_words_path):
    processed_text = ""
    stop_words_list = load_stop_words(stop_words_path)
    # print(stop_words_list)
    for word in word_tokenize_vi(text):
        if word.lower() not in stop_words_list:
            processed_text += " " +  (word)
    # stop_words_pattern = build_stop_word_regex(stop_words_list)
    # tmp = re.sub(stop_words_pattern, '|', text.strip())
    return (processed_text)


class Keywork():
	def __init__(self, keywork, val):
		self.keywork = keywork
		self.val = val