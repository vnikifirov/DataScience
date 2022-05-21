#! /usr/bin/env python
# -*- coding: utf-8 -*-

import nltk # the master library for NLP
import not_comperative_superlative  # my func to convert adj for positive form



#use that part of code, if stopwords not downloaded
#import nltk
#nltk.download("stopwords")
from nltk.corpus import stopwords # prepossessing.
from nltk.corpus import wordnet # exaples from sendex NLP
from nltk.tokenize import word_tokenize # to to remove stop words and to tokenize by words

from pattern.en import parsetree # to grow the word tree
from pattern.en import pluralize, singularize,NOUN, ADJECTIVE # for parsing nouns
from pattern.en import comparative, superlative # comperative and superlative adjunction
from pattern.en import conjugate, lemma, lexeme # module to work with verbs
from pattern.en import tenses, PAST, PL # work with tenses of verb
from pattern.en import verbs, conjugate, PARTICIPLE # Rule-based conjugation
#from nltk.corpus import wordnet as wn # module for WordNet maybe that part can be remove

#from pattern.en import wordnet # module for WordNet/ that wordnet not so good





#from pattern.en import VERB = "VB"#, NOUN, ADJECTIVE, ADVERB = "VB", "NN", "JJ", "RB") in the end- remove that part, if you will not use it


# from the description pattern.en module, I would like to add modules
# thet modules can to help in tuning standard functions from NLTK, pattern.en . And compose work with it like the classes and the part of speech.
from itertools import izip, chain
try:
    from config import SLASH
    from config import WORD, POS, CHUNK, PNP, REL, ANCHOR, LEMMA
    MBSP = True # Memory-Based Shallow Parser for Python.
except:
    SLASH, WORD, POS, CHUNK, PNP, REL, ANCHOR, LEMMA = \
        "&slash;", "word", "part-of-speech", "chunk", "preposition", "relation", "anchor", "lemma"
    MBSP = False



# grabbing words from the input line. Brake line on sentenses. Brake santenses on words.
# and make tags for all words.
def parse_text(text):
    buffer_parsetree_list = []
    parsetree_str = parsetree(text, tokenize=True, tags=True, chunks=True, relations=False, lemma=True, encoding="utf-8", tagset=None)
    for sentence in parsetree_str:
        for chunk in sentence.chunks:
            for word in chunk.words:
                buffer_parsetree_list.append(word)
    return (buffer_parsetree_list)


# function normalaze
# make parse tree with return part of speech, and word form
# The func I taken from the description standard functions in pattern.in module
def word_normalize(text):
    normal_form = parse_text(text)

    # tags for detection part of speech
    Nouns_tags = ["NNS", "NNPS"]
    Adjective_tags = ["JJR", "JJS"]
    Verb_tags = ["VBD", "VBG", "VBN", "VBP", "VBZ"]

    buff_string = [] # buffer list for compose internal box


    # to make noun singular form. The func I taken from standard functions in pattern.in module
    # in that part of code I wish compare tag NNS, NNPS and object from word class.
    for word in normal_form:
        if word.tag in Nouns_tags:
            buff_Noun = singularize(word.string, pos = NOUN)  # make singular from plural
            buff_Noun= str(buff_Noun)
            buff_string.append(buff_Noun)
            return buff_string # how can I return part of speech? Or I need one func just for detecting tag part of speech?
                                 # but that not effective
        else:
            buff_string.append(str(word.string))
            return buff_string


    # make the basic adjective form.
    # in that part of code I wish compare tags JJR, JJS and object from word class
    # and make word singular form, after that use func  not_comperative_superlative to make
    # adj basic form.
    buff_string1 = buff_string
    for word in normal_form:
        if word.tag in Adjective_tags:
            buff_Adj = singularize(word.string, pos = ADJECTIVE)  # make singular from plural
            buff_Adj = str(buff_Adj)
            buff_string1.append.not_comperative_superlative(buff_Adj)
            return buff_string
        else:
            buff_string.append(str(word.string))
            return buff_string


    # verb to infinitive form. The func I taken from standard functions in pattern.in module
    buff_string2 = buff_string # make a copy of entered string
    for word in normal_form:   # go thru the string word by word
        if word.tag in Verb_tags: # looking for only verb
            buff_Vb = str(word.string)
            buf = lemma(buff_Vb)
            buff_string2.append(buf)
            return buff_string2
        else:
            buff_string2.append(str(word.string))
            return buff_string





# functiion receives as input a word as a string, a part of speech, as well as a specific form of the word
# and leads the words from the normal form to the initial form: books-> book ...
# some problems. How can I receive parts_of_speech from previous funcs?
# Eee, I can send in arguments only important part for that part of speech
def word_denormalize(word,part_of_speech,word_form):
    original_word_view = ""
    # decision tree for part of speech

    # Nouns. From singular to plural
    # maybe in that part I need use *args to send any arguments
    if part_of_speech in Nouns_tags and word_form == '?': # I don't understand what I need to send in word_form
        original_word_view = pluralize(word, pos=NOUN, classical=True)
        return original_word_view




"""
    # Adjective. From singular to plural
    # From positive form to comparative or superlative form
    elif part_of_speech in Adjective_tags and word_for == '?':

        if word_form == "comparative" and word_form == "?": # comperlative func and word form make from singulat to plural
            buff = pluralize(word, pos=ADJECTIVE, classical=True)
            original_word_view = comparative(buff)
            return original_word_view

        elif word_form == "superlative" and word_form == "?": # superlative func and word form make from singulat to plural
            buff = pluralize(word, pos=ADJECTIVE, classical=True)
            original_word_view = superlative(buff)
            return original_word_view

        elif word_form == "comparative" and word_form == "?":  # comperlative func and word for singular, for for plural.
            original_word_view = comparative(word)
            return original_word_view

        elif word_form == "superlative" and word_form == "?":  # superlative func and word for singular, for for plural
            original_word_view = superlative(word)
            return original_word_view
"""






"""

    # Verb conjugation.
    # how can I select time, person, number, mood, aspect, negated, parse?
    # what func can use in that part of code?
    #
    elif part_of_speech in Verb_tags and word_for == '?':
        conjugate(verb, tense=PRESENT, person=3, number=SINGULAR, mood=INDICATIVE, aspect=IMPERFECTIVE, negated=False, parse=True)
"""














# that part need to be fix
# the get_synonyms function, which receives the input word in normal form, a part of speech and returns a list of synonyms for this word:
# not workted part, need to be fixed
def get_synonyms(text):
    """

    :param word, part_of_speech:
    :return: list of synonyms
    """
    """
    # try co combine from NLTK examples
    for word in sentence:
        s = wordnet.synset(word)[i] # make synonims for ever word in the xets.
        print(s.synonyms)
        print("ky")
    """


    # example from sendex NLP
    # or I would like to use that list of synonims
    # work with word, not sentence in that part

    synonyms = []

    for syn in wordnet.synset(word):
        for lem in sys.lemmas():
            synonyms.append(lem.name())






# The other parts of speech are NOUN, ADJ and ADV. A synset is identified with a 3-part name of the form: word.pos.nn:
# the function gets an input and for each incoming word gets a list of synonyms, reduced to the form in which it appears in the sentence
def get_synonyms_for_sentence(text):
    # good worked part of synonyms in text. But I need convert in form word in original sentence
    synonyms = []

    text = ["good", "bad"] # input sentence
    for word in text:
        for syn in wordnet.synsets(word):
            for l in syn.lemmas():
                synonyms.append(l.name())
                #print((syn))
                # if l.antonyms():
                #    antonyms.append(l.antonyms()[0].name())

        print(set(synonyms))
        # print(set(antonyms))

    """
    # need to be added part of code to converting synonyms in form like in original sentence and 
    # output: list of synonyms
    """






# main func is a body of program. It's the main part of OOP stile programming.
# that make programme safe and flexible.
def main(text):
    #text = "Londons, the capitals of England and the United Kingdom, is a 21st-century city with history stretching back to Roman times."
    result = word_normalize(text)

    #text = "Londons, the capitals of England and the United Kingdom, is a 21st-century city with history stretching back to Roman times."
    #text = "Adj are most interesting part of speech"

    parse_text(text)
    result = word_normalize(text)
    #word_denormalize(text,text,text)
    #get_synonyms(text)
    #get_synonyms_for_sentence(text)

if __name__ == "__main__":
    # I need to fix it. Becouse on input what I need? string or words?
    text = "Adj are most interesting part o speech"
    main(text)


# test block. REMOVE it after testing

# just for test singularization and plularization
# remove all after fixing problems
#te = "Londons"
#buff_Noun = singularize(te, pos = NOUN)
#print(buff_Noun)


# just for test adjective basic form:

#test = "fantastic"

#print(comparative(text))
#print(superlative(test))





#word = "was"
#result = lemma(word)
#print(result)
#print(lemma("done"))
