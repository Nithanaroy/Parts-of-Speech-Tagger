__author__ = 'nitinpasumarthy'

SENTENCE_SEPARATOR = '###/###'


class Train:
    def __init__(self, in_file):
        self.input = in_file
        self.a = {}
        self.b = {}
        self.tags = {}

    def compute_a_and_b(self):
        # Compute the counts for a and b
        for s in self.get_sentence():
            lines = s.split("\n")
            if lines is None or len(lines) == 0:
                continue

            pw, pt = lines[0].split('/')
            for l in lines[1:]:     # first line is left as pw, pt are set initially using it
                w, t = l.split("/")
                self.upsert_inc(self.a, pt + t)     # merge states together for key
                self.upsert_inc(self.b, pt + pw)    # merge state and word for key
                self.upsert_inc(self.tags, pt)
                pt = t
                pw = w

            # For when pw takes the last word in the sentence, as the loop breaks
            self.upsert_inc(self.b, pt + pw)    # merge state and word for key
            self.upsert_inc(self.tags, pt)

        # Now normalize the counts to get probabilities
        for si_sj in self.a:
            si = self.get_si_and_sj(si_sj)['si']
            self.a[si_sj] /= float(self.tags[si])

        for sj_o in self.b:
            sj = self.get_sj_and_o(sj_o)['sj']
            self.b[sj_o] /= float(self.tags[sj])

    def get_sj_and_o(self, sj_o):
        """
        Splits the merged state and observation (here word)
        :param sj_o: Merged representative for State j and Observation o
        :return:{'sj': #, 'o': #}
        """
        # Assumption: Tags are one character long
        return {'sj': sj_o[0], 'o': sj_o[1:]}

    def get_si_and_sj(self, si_sj):
        """
        Splits the merged word containing State i and State j
        :param si_sj: Merged representative for State i and State j
        :return: {'si': #, 'sj': #}
        """
        # Assumption: Tags are one character long
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

    def get_sentence(self):
        """
        iteratively returns sentences from the input file
        :return:
        """
        import os

        abs_filepath = os.path.abspath(self.input)
        f = open(abs_filepath)
        lines = f.read().splitlines()       # TODO: May not work if file is huge
        f.close()

        sentence = ""
        for l in lines:
            if l == SENTENCE_SEPARATOR:
                if sentence != "":
                    yield sentence.strip()
                sentence = ""
            else:
                sentence += l + "\n"
