''' This module contains the class
for generating incorrect alternative
answers for a given answer
'''
import gensim.downloader as api
from nltk.tokenize import sent_tokenize, word_tokenize
import random


class IncorrectAnswerGenerator:
    ''' This class contains the methods
    for generating the incorrect answers
    given an answer
    '''

    def __init__(self):
        # model required to fetch similar words
        self.model = api.load("glove-wiki-gigaword-100")

    def get_all_options_dict(self, answer, num_options):
        ''' This method returns a dict
        of 'num_options' options out of
        which one is correct and is the answer
        '''
        similar_words = self.model.similar_by_word(answer, topn=15)[::-1]
        options_dict = dict()

        for i in range(1, num_options + 1):
            options_dict[i] = similar_words[i - 1][0]

        replacement_idx = random.randint(1, num_options)

        options_dict[replacement_idx] = answer

        return options_dict
