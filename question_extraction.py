'''This file contains the module for generating
'''
import nltk
import spacy
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer


class QuestionExtractor:
    ''' This class contains all the methods
    required for extracting questions from
    a given document
    '''

    def __init__(self, num_questions):

        self.num_questions = num_questions

        # hash set for fast lookup
        self.stop_words = set(stopwords.words('english'))

        # named entity recognition tagger
        self.ner_tagger = spacy.load('en_core_web_md')

        self.vectorizer = TfidfVectorizer()

        self.questions_dict = dict()

    def get_questions_dict(self, document):
        '''
        Returns a dict of questions in the format:
        question_number: {
            question: str
            answer: str
        }

        Params:
            * document : string
        Returns:
            * dict
        '''
        # find candidate keywords
        self.candidate_keywords = self.get_candidate_entities(document)

        # set word scores before ranking candidate keywords
        self.set_tfidf_scores(document)

        # rank the keywords using calculated tf idf scores
        self.rank_keywords()

        # form the questions
        self.form_questions()

        return self.questions_dict

    def get_filtered_sentences(self, document):
        ''' Returns a list of sentences - each of
        which has been cleaned of stopwords.
        Params:
                * document: a paragraph of sentences
        Returns:
                * list<str> : list of string
        '''
        sentences = sent_tokenize(document)  # split documents into sentences

        return [self.filter_sentence(sentence) for sentence in sentences]

    def filter_sentence(self, sentence):
        '''Returns the sentence without stopwords
        Params:
                * sentence: A string
        Returns:
                * string
        '''
        words = word_tokenize(sentence)
        return ' '.join(w for w in words if w not in self.stop_words)

    def get_candidate_entities(self, document):
        ''' Returns a list of entities according to
        spacy's ner tagger. These entities are candidates
        for the questions

        Params:
                * document : string
        Returns:
                * list<str>
        '''
        entities = self.ner_tagger(document)
        entity_list = []

        for ent in entities.ents:
            entity_list.append(ent.text)

        return list(set(entity_list))  # remove duplicates

    def set_tfidf_scores(self, document):
        ''' Sets the tf-idf scores for each word'''
        self.unfiltered_sentences = sent_tokenize(document)
        self.filtered_sentences = self.get_filtered_sentences(document)

        self.word_score = dict()  # (word, score)

        # (word, sentence where word score is max)
        self.sentence_for_max_word_score = dict()

        tf_idf_vector = self.vectorizer.fit_transform(self.filtered_sentences)
        feature_names = self.vectorizer.get_feature_names()
        tf_idf_matrix = tf_idf_vector.todense().tolist()

        num_sentences = len(self.unfiltered_sentences)
        num_features = len(feature_names)

        for i in range(num_features):
            word = feature_names[i]
            self.sentence_for_max_word_score[word] = ""
            tot = 0.0
            cur_max = 0.0

            for j in range(num_sentences):
                tot += tf_idf_matrix[j][i]

                if tf_idf_matrix[j][i] > cur_max:
                    cur_max = tf_idf_matrix[j][i]
                    self.sentence_for_max_word_score[word] = self.unfiltered_sentences[j]

            # average score for each word
            self.word_score[word] = tot / num_sentences

    def get_keyword_score(self, keyword):
        ''' Returns the score for a keyword
        Params:
            * keyword : string of possible several words
        Returns:
            * float : score
        '''
        score = 0.0
        for word in word_tokenize(keyword):
            if word in self.word_score:
                score += self.word_score[word]
        return score

    def get_corresponding_sentence_for_keyword(self, keyword):
        ''' Finds and returns a sentence containing
        the keywords
        '''
        words = word_tokenize(keyword)
        for word in words:

            if word not in self.sentence_for_max_word_score:
                continue

            sentence = self.sentence_for_max_word_score[word]

            all_present = True
            for w in words:
                if w not in sentence:
                    all_present = False

            if all_present:
                return sentence
        return ""

    def rank_keywords(self):
        '''Rank keywords according to their score'''
        self.candidate_triples = []  # (score, keyword, corresponding sentence)

        for candidate_keyword in self.candidate_keywords:
            self.candidate_triples.append([
                self.get_keyword_score(candidate_keyword),
                candidate_keyword,
                self.get_corresponding_sentence_for_keyword(candidate_keyword)
            ])

        self.candidate_triples.sort(reverse=True)

    def form_questions(self):
        ''' Forms the question and populates
        the question dict
        '''
        used_sentences = list()
        idx = 0
        cntr = 1
        num_candidates = len(self.candidate_triples)
        while cntr <= self.num_questions and idx < num_candidates:
            candidate_triple = self.candidate_triples[idx]

            if candidate_triple[2] not in used_sentences:
                used_sentences.append(candidate_triple[2])

                self.questions_dict[cntr] = {
                    "question": candidate_triple[2].replace(
                        candidate_triple[1],
                        '_' * len(candidate_triple[1])),
                    "answer": candidate_triple[1]
                }

                cntr += 1
            idx += 1
