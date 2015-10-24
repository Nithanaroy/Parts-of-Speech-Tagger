__author__ = 'nitinpasumarthy'


class Tagger:
    def __init__(self, hmm_model, sentence):
        """
        Constructor for tagger class
        :param hmm_model: Model trained on HMM with A and B lists
        :param sentence: sentence to tag, with one word on each line
        :return: tagger object
        """
        self.model = hmm_model
        self.sentence = hmm_model.clean_sentence(sentence)

    def tag(self):
        v = list()
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
            key_for_b = self.model.get_key_from_stateobv_for_b(dest_state, word)
            try:
                vij[source_state] = v[t - 1][source_state] * self.model.a[key_for_a] * self.model.b[key_for_b]
            except KeyError:
                # some keys might not be defined by train set.
                vij[source_state] = 0
        return vij

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
