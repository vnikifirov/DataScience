#from nltk.corpora import wordnet as wn # adding nouns dictinary
#import nltk
#import wordnet as wn
#for synset in list(wn.all_synsets(wn.NOUN)):
#    print synset

# my code like idea is here, but invisible, I must fix it and make it visible

VOWELS = "aeiouy"
CONSONANTS = "bcdfghjklmnpqrstvwxyz"
DOUBLE_CONSONANTS = "bb","cc","dd","ff","gg","hh","jj","kk","ll","mm","nn","pp","qq","rr","ss","tt","vv","ww","xx","yy","zz"


# try to make plural nouns from noun and try to find it plural noun in dictionary
# in adj use bad, many. Maybe it can little bit improve accuracy


# I can solve that problem without func comperlative and superlative, but I need en dictionary with comprative- superlative adj
#

# how to write automated test, or just simple test for cheking adj ans noun functions?
# how to testing work?
# fot automated testing I need files with correct form and answer, read that file and take back answer of func comperative_superlative
#

grade_irregular = {
    "worse":"bad",
    "worst":"bad",
    "further":"far",
    "farthest":"far",
    "better":"good",
    "best":"good",
    "hinder":"hind",
    "hindmost":"hind",
    "lesser":"less",
    "least":"less",
    "less":"little",
    "most":"much",
    "more":"much"}

grade_uninflected = ["giant", "glib", "hurt", "known", "madly"]
full_grade_uninflected = ["more giant", "most giant", "more glib","most glib", "more hurt","most hurt", "more known","most known", "more madly","most madly",]

COMPARATIVE = "er"   # need to substract er
SUPERLATIVE = "est"  # need to substact est

def _count_syllables(word):
    """ Returns the estimated number of syllables in the word by counting vowel-groups."""

    n = 0
    p = False # True if the previous character was a vowel.
    for ch in word.endswith("e") and word[:-1] or word:
        v = ch in VOWELS
        n += int(v and not p)
        p = v # pairs of syllables,
    print(n)
    return n

def grade(adjective):
    """ Returns the comparative or superlative form of the given adjective."""
    n = _count_syllables(adjective)
    if adjective in grade_irregular:
        # A number of adjectives inflect irregularly.
        return grade_irregular.get(adjective) # comparative. Receive the basic form from the key. That part are done

    # A number of adjectives don't inflect at all.
    elif adjective in grade_uninflected:
        return (adjective) # just return adjective without changing

    # I need to subtract suffix and remove more or most/ I to remove the first word in phrase
    elif adjective in full_grade_uninflected: # check that part. It's correct?
        index = 0
        for letter in adjective:
            if letter != " ":
                index += 1
                continue
            else:
                adjective = adjective[index:]
                #print(adjective)
                return (adjective)


# that part of code worked
    # removing endswith "est" like that:  hottest -> hot
    elif (len(word)>= 6 and adjective[-3:] in ("est") and adjective[-5:-3] in DOUBLE_CONSONANTS):
        adjective = adjective[:-4]
        return adjective

    # removing endswith "er" like that:  hotter -> hot
    elif (len(word)>= 6 and adjective[-2:] in ("er") and adjective[-4:-2] in DOUBLE_CONSONANTS):
        adjective = adjective[:-3]
        return adjective


    # Also included are disyllabic words ending in -ble, -er, -y, -some, -ow:
    # some trubles here! try to fix it by func with endwith -ble, -er, -y, -some, -ow
    # removing endswith "est" like that:  largest -> large
    elif ( n>=2 and len(word)>= 6 and adjective[-3:] in ("est") and adjective[-4:-3] in CONSONANTS  and adjective[-5:-3] not in ("ble", "er", "y", "some", "ow")):
        print(adjective[-5:-3])
        adjective = adjective[:-2]
        return adjective

    # Also included are disyllabic words ending in -ble, -er, -y, -some, -ow:
    # removing endswith "est" like that:  larger -> large
    elif (len(word) >= 6 and adjective[-2:] in ("er") and adjective[-3:-2] in CONSONANTS and adjective[-4:-2] not in ("ble", "er", "y", "some", "ow")):
        #print(adjective[-4:-3])
        #print("123")
        adjective = adjective[:-1]
        return adjective


    # removing endswith "est" like that:  easiest -> easy
    elif (len(word) >= 6 and adjective[-2:] in ("est") and adjective[-4:-3] == 'i'):
        # print(adjective[-4:-3])
        # adjective = adjective[:-3]
        adjective = adjective[:-4] + "y"
        return adjective

    # removing endswith "er" like that:  easier -> easy
    elif (len(word)>= 6 and adjective[-2:] in ("er") and adjective[-3:-2] == 'i'):
        #print(adjective[-3:-2])
        adjective = adjective[:-3]
        adjective = adjective+"y"
        return adjective

    # narrowest -> narrower
    elif ( n==3 and adjective[-3:] in ("est")): # and adjective[-5:-3] in CONSONANTS ):
        # print(adjective[-5:-3])
        adjective = adjective[:-3]
        return adjective

    elif ( n==3 and adjective[-2:] in ("er")): # and adjective[-5:-3] in CONSONANTS ):
        # print(adjective[-5:-3])
        adjective = adjective[:-2]
        return adjective

# that words can't pass the test. Need to be fixed
      # softest -> soft
      # newest -> new
      # newer new
      # most effective, more effective -> effective


def not_compar_not_super(adjective):
    return grade(adjective)


# just for test adjective basic form:
# remove it after fix the func

#word = "newer"
#word = "newest"
#word = "oldest"

#print(not_compar_not_super(word))
