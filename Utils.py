__author__ = 'nitinpasumarthy'

SENTENCE_SEPARATOR = '###/###'
DEBUG = True


def get_sentence(filepath):
    """
    iteratively returns sentences from the input file
    :return:
    """
    import os

    abs_filepath = os.path.abspath(filepath)
    f = open(abs_filepath)
    lines = f.read().splitlines()  # TODO: May not work if file is huge
    f.close()

    sentence = ""
    for l in lines:
        if l == SENTENCE_SEPARATOR:
            if sentence != "":
                yield clean_sentence(sentence)
            sentence = ""
        else:
            sentence += l + "\n"


def get_count_of_sentences(filepath):
    import os

    abs_filepath = os.path.abspath(filepath)
    with open(abs_filepath) as f:
        return f.read().count(SENTENCE_SEPARATOR) - 1


def write_sentence(f, sentence):
    """
    Writes the given sentence surrounded from top by SENTENCE_SEPARATOR
    :param f: open file handle
    :param sentence: sentence to write
    """
    f.write(SENTENCE_SEPARATOR + "\n" + sentence + "\n")


def clean_sentence(sentence):
    """
    Clean the setence - stemming, change to lower case etc...
    :param sentence: sentence to clean
    :return: cleaned sentence
    """
    return sentence.strip()
