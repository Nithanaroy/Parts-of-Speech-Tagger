__author__ = 'nitinpasumarthy'

import Utils
import os
from Train import Train
from Tagger import Tagger

import logging

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)


class Test:
    def __init__(self, trainfile, testfile, outfile):
        self.testfile = testfile
        self.trainfile = trainfile
        self.outfile = outfile

        self.model = Train(trainfile)
        logging.info("Training complete...")
        self.save_results()

    def save_results(self):
        abs_filepath = os.path.abspath(self.outfile)

        total = Utils.get_count_of_sentences(self.testfile) * 1.0
        logging.info("{} sentences found".format(total))

        with open(abs_filepath, 'w') as f:
            for i, s in enumerate(Utils.get_sentence(self.testfile)):
                original_sentence = s['o']  # original raw sentence from file
                s = s['c']  # cleaned sentence
                untagged_sentence = self.remove_tags(s)
                untagged_original_sentence = self.remove_tags(original_sentence)
                tags = Tagger(self.model, untagged_sentence).tag()
                tagged_sentence = self.attach_tags(untagged_original_sentence, tags)
                Utils.write_sentence(f, tagged_sentence)

                if i % 100 == 0:
                    logging.info("{}% done. Last tagged: {}".format(round(i / total * 100.0, 2), s.replace("\n", " ")))
                # break

            f.write(Utils.SENTENCE_SEPARATOR)

    def error_rate(self, actual_file, expected_file):
        import os
        abs_actual_file = os.path.abspath(actual_file)
        abs_expected_file = os.path.abspath(expected_file)
        actual_lines = open(abs_actual_file).read().splitlines()  # TODO: May not work if file doesn't fit in memory
        expected_lines = open(abs_expected_file).read().splitlines()  # TODO: May not work if file doesn't fit in memory

        mismatch_count = 0
        total_lines = len(expected_lines)
        matching_count = min(len(actual_lines), total_lines)
        for i in range(0, matching_count):
            if actual_lines[i].lower() != expected_lines[i].lower():  # TODO: Works for ASCII perfectly
                mismatch_count += 1

        mismatch_count += total_lines - matching_count
        return mismatch_count / float(total_lines)

    def attach_tags(self, sentence, tags):
        """
        Creates a sentence of the form word/tag taking words from 'sentence'
        and tag for that word from 'tags'
        :param sentence: sentence to tag with one word per line
        :param tags: corresponding tags for each word
        :return: tagged sentence with word/its_tag one per line
        """
        words = sentence.split('\n')
        tags = [tag.upper() for tag in tags]  # Always print tags in upper case
        return '\n'.join([w + "/" + t for w, t in zip(words, tags)])

    def remove_tags(self, sentence):
        """
        Removes parts of speech tags (if any) for the given sentence
        :param sentence: source sentence with one word per line
        :return: sentence stripped of parts of speech
        """
        lines = sentence.split("\n")
        if lines is None or len(lines) == 0:
            return

        cleaned_sentence = ""
        for l in lines:
            w_t = l.split("/")  # word and tag
            cleaned_sentence += w_t[0] + "\n"  # again save one word per line

        return cleaned_sentence.strip()
