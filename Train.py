__author__ = 'nitinpasumarthy'

import Utils

START_STATE_SYMBOL = 'A'    # Beware of the assumption that it should be only 1 character


class Train:
    def __init__(self, in_file):
        self.input = in_file
        self.start_state_symbol = START_STATE_SYMBOL
        self.a = {}
        self.b = {}
        self.states = {}

        self.compute_a_and_b()

    def compute_a_and_b(self):
        # Compute the counts for a and b
        for s in Utils.get_sentence(self.input):
            lines = s.split("\n")
            if lines is None or len(lines) == 0:
                continue

            pt = START_STATE_SYMBOL  # start of a sentence - Start Tag
            for l in lines:
                w, t = l.split("/")
                self.upsert_inc(self.a, self.get_key_from_states_for_a(pt, t))
                self.upsert_inc(self.b, self.get_key_from_stateobv_for_b(t, w))
                self.upsert_inc(self.states, pt)
                pt = t

            # For when pt takes the last word/tag in the sentence, as the loop breaks
            self.upsert_inc(self.states, pt)
            # break

        # Now normalize the counts to get probabilities
        for si_sj in self.a:
            si = self.get_states_from_key_of_a(si_sj)['si']
            self.a[si_sj] /= float(self.states[si])

        for sj_o in self.b:
            sj = self.get_stateobv_from_key_of_b(sj_o)['sj']
            self.b[sj_o] /= float(self.states[sj])

    def get_key_from_states_for_a(self, source_state, destination_state):
        """
        Creates a key string to be used in self.'a' dictionary
        :param source_state: State i
        :param destination_state: State j
        :return: key using states
        """
        return source_state + destination_state

    def get_key_from_stateobv_for_b(self, state, observation):
        """
        Creates a key from state and observation for using in self.'b' dictionary
        :param state: State j
        :param observation: Observation Vk
        :return: a key
        """
        return state + observation

    def get_stateobv_from_key_of_b(self, sj_o):
        """
        Splits the merged state and observation (here word)
        :param sj_o: Merged representative for State j and Observation o
        :return:{'sj': #, 'o': #}
        """
        # Assumption: Tags are one character long
        return {'sj': sj_o[0], 'o': sj_o[1:]}

    def get_states_from_key_of_a(self, si_sj):
        """
        Splits the merged word containing State i and State j
        :param si_sj: Merged representative for State i and State j
        :return: {'si': #, 'sj': #}
        """
        # Assumption: States are one character long
        return {'si': si_sj[0], 'sj': si_sj[1]}

    def upsert_inc(self, dictionary, key):
        """
        Checks the key in this dictionary and increments the value if found
        else a key is created and value of 1 is set
        :return: None
        """
        if key in dictionary:
            dictionary[key] += 1
        else:
            dictionary[key] = 1
