#!/usr/bin/env python
import argparse
import sys
import codecs
import string
import itertools

if sys.version_info[0] == 2:
  from itertools import izip
else:
  izip = zip
from collections import defaultdict as dd
import re
import os.path
import gzip
import tempfile
import shutil
import atexit

# Use word_tokenize to split raw text into words
from string import punctuation

import nltk
from nltk.tokenize import word_tokenize

scriptdir = os.path.dirname(os.path.abspath(__file__))

reader = codecs.getreader('utf8')
writer = codecs.getwriter('utf8')

def prepfile(fh, code):
  if type(fh) is str:
    fh = open(fh, code)
  ret = gzip.open(fh.name, code if code.endswith("t") else code+"t") if fh.name.endswith(".gz") else fh
  if sys.version_info[0] == 2:
    if code.startswith('r'):
      ret = reader(fh)
    elif code.startswith('w'):
      ret = writer(fh)
    else:
      sys.stderr.write("I didn't understand code "+code+"\n")
      sys.exit(1)
  return ret

def addonoffarg(parser, arg, dest=None, default=True, help="TODO"):
  ''' add the switches --arg and --no-arg that set parser.arg to true/false, respectively'''
  group = parser.add_mutually_exclusive_group()
  dest = arg if dest is None else dest
  group.add_argument('--%s' % arg, dest=dest, action='store_true', default=default, help=help)
  group.add_argument('--no-%s' % arg, dest=dest, action='store_false', default=default, help="See --%s" % arg)



class LimerickDetector:

    def __init__(self):
        """
        Initializes the object to have a pronunciation dictionary available
        """
        self._pronunciations = nltk.corpus.cmudict.dict()
        # CMU dictionary returns upper case letters, thus we use upper case, too
        # symbols of syllables in CMU dictionary
        self._syllables = ['AA','AE','AH' ,'AO' ,'AW' ,'AX' ,'AXR','AY' ,'EH' ,'ER' ,'EY' ,'IH' ,'IX' ,'IY' ,'OW' ,'OY' ,'UH' ,'UW', 'UX']


    def num_syllables(self, word):
        """
        Returns the number of syllables in a word.  If there's more than one
        pronunciation, take the shorter one.  If there is no entry in the
        dictionary, return 1.
        """
        #print self._pronunciations[word]
        #print sum([1 for x in self._pronunciations if x not in self.consonants])
        if word in self._pronunciations:
            # count syllables(vowels) by counting elements not in consonants list
            # and then, take min to return shorter one
            # for comparison, take digits at the end off
            # digits are stresses
            return min([sum([1 for j in i if j[:2] in self._syllables]) for i in self._pronunciations[word]])
        else:
            # no entry in dictionary, return 1
            return 1

    def rhymes(self, a, b):
        """
        Returns True if two words (represented as lower-case strings) rhyme,
        False otherwise.
        """
        # first strip until 1st vowel is found
        # comapre length
        # check rhyme

        # if word a or b is not in pronunciation dictionary,
        # a & b doesn't rhyme
        if a not in self._pronunciations or b not in self._pronunciations:
            # print 'Either of a or b is not in pronunciation dictionary'
            return False

        # for case word having more than one pronunciation
        a_rs = []
        b_rs = []

        # for each pronunciation
        for ai in self._pronunciations[a]:
            for i, k in enumerate(ai):
                # if first vowel is found
                if k[:2] in self._syllables:
                    # store striped tokens
                    a_rs.append(ai[i:])
                    # stop search
                    break

        for bi in self._pronunciations[b]:
            for i, k in enumerate(bi):
                # if first vowel is found
                if k[:2] in self._syllables:
                    # store striped tokens
                    b_rs.append(bi[i:])
                    # stop search
                    break
        # print 'a', a_rs
        # print 'b', b_rs
        # comb = productino of pronunciation list of a and b
        rhyme_flag = False
        for comb in itertools.product(a_rs, b_rs):
            # if 1st is shorter or same, then choose 1st as shorter one
            # shorter one has to be prefix or suffix of longer one
            if len(comb[0]) <= len(comb[1]):
                shorter = 0
                longer = 1
            else:
                shorter = 1
                longer = 0

            # print 'shorter', comb[shorter]
            # print 'longer ', comb[longer]
            # check prefix rhyme
            match_cnt = 0
            for i, k in enumerate(comb[shorter]):
                # print 'prefix check - i:%d, k:%s' % (i, k)
                # if there is non-match during check, this isn't rhyme
                # don't need to proceed
                # print 'prefix-k:%s, lk:%s' % (k, comb[longer][i]), k==comb[longer][i]
                if k != comb[longer][i]:
                    break
                else:
                # otherwise, increase match count
                    match_cnt += 1
            # if match_cnt equal to len(comb[shoter]), shorter one is
            # a prefix of longer one
            if match_cnt == len(comb[shorter]):
                # change flag to True and stop rhyme check
                rhyme_flag = True
                return True
                # break

            # check suffix(from end)
            match_cnt = 0
            # iterate from the end by using built-in function 'reversed'
            # need to add difference of longer and shorter to index
            # when compare shorter to longer, because of length difference
            dif = len(comb[longer])-len(comb[shorter])
            for i, k in reversed(list(enumerate(comb[shorter]))):
                # if there is non-match during check, this isn't rhyme
                # don't need to proceed
                # print 'suffix check - i:%d, k:%s' % (i, k)
                # print 'suffix-k:%s, lk:%s' % (k, comb[longer][i+dif]), k == comb[longer][i+dif]
                # print 'i:%d, k:%s' % (i, k)
                if k != comb[longer][i+dif]:
                    break
                else:
                    # otherwise, increase match count
                    match_cnt += 1

            # if match_cnt equal to len(comb[shoter]), shorter one is
            # a prefix of longer one
            if match_cnt == len(comb[shorter]):
                # change flag to True and stop rhyme check
                rhyme_flag = True
                return True
                # break

        # if flow comes until here, then there is no rhyme match
        # return False
        return False

    def is_limerick(self, text):
        """
        Takes text where lines are separated by newline characters.  Returns
        True if the text is a limerick, False otherwise.

        A limerick is defined as a poem with the form AABBA, where the A lines
        rhyme with each other, the B lines rhyme with each other, and the A lines do not
        rhyme with the B lines.


        Additionally, the following syllable constraints should be observed:
          * No two A lines should differ in their number of syllables by more than two.
          * The B lines should differ in their number of syllables by no more than two.
          * Each of the B lines should have fewer syllables than each of the A lines.
          * No line should have fewer than 4 syllables

        (English professors may disagree with this definition, but that's what
        we're using here.)


        """
        # unicode escape, lower, and then split with newline character to get each line
        # if the length of each line after strip to get rid of white space
        # is not 0, then do word_tokenization
        # also, from word_tokenizatino result, remove punctuation by checking
        # with string.punctuation

        # if input text is not string, return False
        if type(text) != str:
            return False
        # print 'before', type(text)==str, text
        tk_list = [[x for x in word_tokenize(s) if x not in punctuation]
                   for s in text.decode('unicode_escape').lower().split('\n')
                   if len(s.strip()) != 0]
        # temp = [word_tokenize(s)
        #           for s in text.decode('unicode_escape').lower().split('\n')
        #           if len(s.strip()) != 0]

        # if text is not consisted by 5 lines, return False
        if len(tk_list) != 5:
            return False

        # print len(tk_list)
        # for tk in tk_list:
            # print len(tk), tk

        # syllables check
        a_syl = []
        b_syl = []
        for i, k in enumerate(tk_list):
            if i in [0,1,4]:  # A lines
                a_syl.append(sum([self.num_syllables(x) for x in k]))
            else:  # B lines
                b_syl.append(sum([self.num_syllables(x) for x in k]))
        # print 'Syllable check'
        # print 'A lines', a_syl
        # print 'B lines', b_syl

        # check no two A lines should  differ in their number of syllables
        #  by more than two. If max(a_syl)-min(a_syl) is larger than 2,
        # then there is at least 1 pair of A lines that different larger than 2
        if max(a_syl) - min(a_syl) > 2:
            return False

        # B lines should differ in their number of syllables by no more than two
        if max(b_syl) - min(b_syl) > 2:
            return False

        # Each of B lines should have fewer syllables than each of the A lines
        if min(a_syl) - max(b_syl) <= 0:
            return False

        # No line should have fewer than 4 syllables
        if min(a_syl+b_syl) < 4:
            return False


        a_last = []
        b_last = []
        for i, k in enumerate(tk_list):
            if i in [0,1,4]:  # A lines
                a_last.append(k[-1])  # get last word for rhyme check
            else:
                b_last.append(k[-1])  # get last word for rhyme check

        # all words in a_last and b_last should be rhyme respectively
        # print 'Rhyme check for A lines and B lines'
        # print 'A'
        for i in itertools.combinations(a_last, 2):
            # print self.rhymes(i[0], i[1])
            if not self.rhymes(i[0], i[1]):
                # if not rhyme, return False
                return False
        # print 'B'
        for i in itertools.combinations(b_last, 2):
            # print self.rhymes(i[0], i[1])
            if not self.rhymes(i[0], i[1]):
                # if not rhyme, return False
                return False
        # print 'A-B'
        for i in itertools.product(a_last, b_last):
            # print self.rhymes(i[0], i[1])
            if self.rhymes(i[0], i[1]):
                # if rhyme, return False
                return False

        # print('--------------done-----------')
        # if got here, Syllable and rhyme test passed
        return True


# The code below should not need to be modified
def main():
  parser = argparse.ArgumentParser(description="limerick detector. Given a file containing a poem, indicate whether that poem is a limerick or not",
                                   formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  addonoffarg(parser, 'debug', help="debug mode", default=False)
  parser.add_argument("--infile", "-i", nargs='?', type=argparse.FileType('r'), default=sys.stdin, help="input file")
  parser.add_argument("--outfile", "-o", nargs='?', type=argparse.FileType('w'), default=sys.stdout, help="output file")




  try:
    args = parser.parse_args()
  except IOError as msg:
    parser.error(str(msg))

  infile = prepfile(args.infile, 'r')
  outfile = prepfile(args.outfile, 'w')

  ld = LimerickDetector()
  lines = ''.join(infile.readlines())
  outfile.write("{}\n-----------\n{}\n".format(lines.strip(), ld.is_limerick(lines)))

if __name__ == '__main__':
  main()
