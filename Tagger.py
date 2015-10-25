__author__ = 'nitinpasumarthy'

import Utils


class Tagger:
    def __init__(self, hmm_model, sentence):
        """
        Constructor for tagger class
        :param hmm_model: Model trained on HMM with A and B lists
        :param sentence: sentence to tag, with one word on each line
        :return: tagger object
        """
        self.model = hmm_model
        self.sentence = Utils.clean_sentence(sentence)  # Clean the sentence to tag
        self.unknown_words = []

    def tag(self):
        v = list()  # state probabilities for each observation
        v.append(self.get_v1())
        words = self.sentence.split('\n')[1:]  # First word is already used for computing v1
        for i, w in enumerate(words):
            t = i + 1
            vj = {}
            for state in self.model.states:
                vij = self.compute_vij(v, t, state, w)
                best_source_state = max(vij, key=lambda k: vij[k])  # Can save this for back pointer
                vj[state] = vij[best_source_state]
            v.append(vj)
        # return the best tag for each observation
        return [max(y, key=lambda k: y[k]) for y in v]

    def compute_vij(self, v, t, dest_state, word):
        vij = {}
        for source_state in self.model.states:
            key_for_a = self.model.get_key_from_states_for_a(source_state, dest_state)
            try:
                vij[source_state] = v[t - 1][source_state] * self.model.a[key_for_a] * self.get_bjk(dest_state, word)
            except KeyError:
                # some transitions might not be defined by train set.
                vij[source_state] = 0
        return vij

    def get_bjk(self, state, word):
        """
        Computes bjk considering two cases:
            1) Known word from training data: returns the corresponding value from 'b'
            2) Unknown word, not seen in training data: assigning equal probability for this transition for all states
        :param state: state from which the transition started - the 'j' value of bjk in HMM
        :param word: observation in HMM, the 'k' value in bjk
        :return: bjk
        """
        bjk = 1.0 / len(self.model.states)  # initialize as if it is an unknown word
        if word in self.unknown_words:
            return bjk

        known_word = False  # will be set to true if the word is found in the training data
        for _state in self.model.states:
            key_for_b = self.model.get_key_from_stateobv_for_b(_state, word)
            if key_for_b in self.model.b:
                known_word = True
                break

        if known_word:
            key_for_b = self.model.get_key_from_stateobv_for_b(state, word)
            bjk = self.model.b[key_for_b]
        else:
            self.unknown_words.append(word)

        return bjk

    def get_v1(self):
        start_state = self.model.start_state_symbol
        v1 = {}
        word0 = self.sentence.split('\n')[0]
        for state in self.model.states:
            key_for_a = self.model.get_key_from_states_for_a(start_state, state)
            key_for_b = self.model.get_key_from_stateobv_for_b(state, word0)
            try:
                v1[state] = self.model.a[key_for_a] * self.model.b[key_for_b]
            except KeyError:
                # some keys might not be defined by train set.
                v1[state] = 0
        return v1
