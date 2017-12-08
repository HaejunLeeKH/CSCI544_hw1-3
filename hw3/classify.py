#!/usr/bin/env python
from collections import defaultdict
from csv import DictReader, DictWriter

import nltk
import codecs
import sys
from nltk.corpus import wordnet as wn
from nltk.tokenize import TreebankWordTokenizer
import gzip
import cPickle as pickle

kTOKENIZER = TreebankWordTokenizer()

def morphy_stem(word):
    """
    Simple stemmer
    """
    stem = wn.morphy(word)
    if stem:
        return stem.lower()
    else:
        return word.lower()


def ngrams(sequence, n):
    # sequence: sequence of words, list
    # n: degree of ngrams

    iter_seq = iter(sequence)
    history = []
    # make first n-1 elements ready
    while n > 1:
        history.append(next(iter_seq))
        n -= 1
    # print(history)
    # print(sequence)

    # add Nth element, yield, and get rid of first element
    # repeat the process
    for item in iter_seq:
        # print(item)
        history.append(item)
        # print(tuple(history))
        yield tuple(history)
        del history[0]


class FeatureExtractor:
    def __init__(self):
        """
        You may want to add code here
        """
        self.fd = pickle.load(open("frequent_data", "rb"))
        self.fre_list = [1,9,10]  # [1,2,9,10] get same result
        self.wd_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        # for wd_list, from 10, 0.02 increased which is 2%
        self.wd_idx = {i:'word_length_'+str(i) for i in self.wd_list}
        self.verb_list = ['VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
        self.adj_list = ['JJ', 'JJR', 'JJS']
        self.ng_fd = pickle.load(open("frequent_ngram", "rb"))


    def features(self, text):
        d = defaultdict(int)
        # initialize word_length with 0
        # wd_idx = {}

        for i in self.wd_list:
            d['word_length_'+str(i)] = 0
            # wd_idx[i] = 'word_length_'+str(i)

        for i in self.fre_list:
            d['FREQUENCY_QUARTILE_' + str(i)] = 0

        # sentence length by # of words and # of chars
        d['SENTENCE_LENGTHBY_WORD'] = 0
        d['SENTENCE_LENGTHBY_CHAR'] = 0

        tokens = kTOKENIZER.tokenize(text)
        # stem_tk = []
        for ii in tokens:
            stemed = morphy_stem(ii)
            d[stemed] += 1
            # stem_tk.append(stemed)

            # word length vector
            if len(ii) not in self.wd_idx and len(ii)>10:
                # if word_length 10 is not found, then increase length 10
                d['word_length_10'] += 1
            elif len(ii) in self.wd_idx:
                d[self.wd_idx[len(ii)]] += 1

            # check frequency quartile info
            if self.fd[ii] in self.fre_list:
                d['FREQUENCY_QUARTILE_' + str(self.fd[ii])] += 1

            # sentence length check
            # d['SENTENCE_LENGTHBY_WORD'] += 1
            d['SENTENCE_LENGTHBY_CHAR'] += len(ii)  # this is better

        # 3 gram increase 0.001
        # for ng in ngrams(tokens, 3):
            # d[ng] += 1
        #d[morphy_stem(ii)] += 1

        # 1st word & 2nd last word. Use 2nd last word because last word is
        # usually punctuation, which is hard to be a style for author
        # Having more than 1 from each side will harm performance
        d['SENTENCE_START_'] = tokens[0]
        # d['SENTENCE_END_1'] = ng[-1]
        d['SENTENCE_END_2'] = tokens[-2]

        pos_tokens = nltk.pos_tag(tokens)

        #d['VERB_COUNT_'] = 0
        # for pos in pos_tokens:
        #    if pos[1] in ['VBD', 'VBG', 'VBN', 'VBP', 'VBZ']:
        #        d['VERB_COUNT_'] += 1

        # count type of verb tag
        for tag in self.verb_list:
            d['VERB_TYPE_'+tag] = 0
        for pos in pos_tokens:
            if 'VERB_TYPE_'+pos[1] in d:
                d['VERB_TYPE_' + pos[1]] += 1

        for tag in self.adj_list:
            d['ADJECTIVE_TYPE_' + tag] = 0
        for pos in pos_tokens:
            if 'ADJECTIVE_TYPE_'+pos[1] in d:
                d['ADJECTIVE_TYPE_' + pos[1]] += 1

        """
        for tag in [ 'RBR', 'RBS', 'WRB']:
            d['ADVERB_TYPE_' + tag] = 0
        for pos in pos_tokens:
            if 'ADVERB_TYPE_'+pos[1] in d:
                d['ADVERB_TYPE_' + pos[1]] += 1
        """
        ng_fre_list = [1,2,3,4,5,6,7,8,9,10]
        for i in ng_fre_list:
            d['NGRAM_FREQUENCY_QUARTILE_' + str(i)] = 0
        for ng in ngrams(pos_tokens, 2):
            if self.ng_fd[ng] in ng_fre_list:
                d['NGRAM_FREQUENCY_QUARTILE_' + str(self.fd[ng])] += 1



        return d


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

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("--trainfile", "-i", nargs='?', type=argparse.FileType('r'), default=sys.stdin, help="input train file")
    parser.add_argument("--testfile", "-t", nargs='?', type=argparse.FileType('r'), default=None, help="input test file")
    parser.add_argument("--outfile", "-o", nargs='?', type=argparse.FileType('w'), default=sys.stdout, help="output file")
    parser.add_argument('--subsample', type=float, default=1.0,
                        help='subsample this fraction of total')
    args = parser.parse_args()
    trainfile = prepfile(args.trainfile, 'r')
    if args.testfile is not None:
        testfile = prepfile(args.testfile, 'r')
    else:
        testfile = None
    outfile = prepfile(args.outfile, 'w')

    # Create feature extractor (you may want to modify this)
    fe = FeatureExtractor()
    
    # Read in training data
    train = DictReader(trainfile, delimiter='\t')
    
    # Split off dev section
    dev_train = []
    dev_test = []
    full_train = []

    for ii in train:
        if args.subsample < 1.0 and int(ii['id']) % 100 > 100 * args.subsample:
            continue
        feat = fe.features(ii['text'])
        if int(ii['id']) % 5 == 0:
            dev_test.append((feat, ii['cat']))
        else:
            dev_train.append((feat, ii['cat']))
        full_train.append((feat, ii['cat']))

    # Train a classifier
    sys.stderr.write("Training classifier ...\n")
    classifier = nltk.classify.NaiveBayesClassifier.train(dev_train)

    right = 0
    total = len(dev_test)
    for ii in dev_test:
        prediction = classifier.classify(ii[0])
        if prediction == ii[1]:
            right += 1
    sys.stderr.write("Accuracy on dev: %f\n" % (float(right) / float(total)))

    if testfile is None:
        sys.stderr.write("No test file passed; stopping.\n")
    else:
        # Retrain on all data
        classifier = nltk.classify.NaiveBayesClassifier.train(dev_train + dev_test)

        # Read in test section
        test = {}
        for ii in DictReader(testfile, delimiter='\t'):
            test[ii['id']] = classifier.classify(fe.features(ii['text']))

        # Write predictions
        o = DictWriter(outfile, ['id', 'pred'])
        o.writeheader()
        for ii in sorted(test):
            o.writerow({'id': ii, 'pred': test[ii]})
