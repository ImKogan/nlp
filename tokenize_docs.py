#!/usr/bin/env python3

'''
tokenize_test.py

'''
import os
from glob import glob
import string
import hashlib
from collections import defaultdict, Counter
from time import time
from nltk import sent_tokenize, word_tokenize, pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn

wnl = WordNetLemmatizer()
lemmatize = wnl.lemmatize

def upenn2wn_tag(tag):
    ''' function to map upenn tags (tags used by default nltk)
    to the tags used by WordNet. This allows WordNet to lemmatize in context.
    '''
    if tag.startswith('J'):
        return wn.ADJ
    elif tag.startswith('V'):
        return wn.VERB
    elif tag.startswith('N'):
        return wn.NOUN
    elif tag.startswith('R'):
        return wn.ADV
    else:
        return 'n'

def lemmatize_sent(sent):
    '''takes tokenized sent as input and return list of lemmas
    '''
    nltk_tagged = pos_tag(sent)
    wn_tagged = map(lambda x: (x[0], upenn2wn_tag(x[1])), nltk_tagged)

    return [lemmatize(word.lower(), pos=upenn2wn_tag(tag))
        for word, tag in nltk_tagged]

def tokenize_doc(
        path,
        hashes={}, sent_dict={},
        word_dict=defaultdict(Counter)):
    ''' perform sentense and word tekenization and store in dicts
    '''
    punctuation = list(string.punctuation)
    punctuation.remove('-')
    punctuation = ''.join(punctuation)
    quotes = ''.join(map(chr, range(8216,8222)))
    doc_name = path.split('/')[-1][:-4]
    
    with open(path, 'rb') as f:
        hasher = hashlib.md5()
        buf = f.read()
        hasher.update(buf)
        hashes[doc_name] = hasher.hexdigest()
        text = buf.decode()
        sent_dict[doc_name] = sent_tokenize(text)
        
        i = 0
        for item in sent_dict[doc_name]:
            if len(item) < 5:
                if not any(x.isalnum() for x in item):
                    del sent_dict[doc_name][i]
                    continue
            sentence = sent_dict[doc_name][i].translate(
                str.maketrans('-', ' ', punctuation+quotes))
            tokenized_text = word_tokenize(sentence)
            lemmas = lemmatize_sent(tokenized_text)
            for j in range(len(tokenized_text)):
                word_dict[(tokenized_text[j], lemmas[j])][(doc_name, i)]+=1
            i+=1

def tokenize_docs(path, hashes={},sent_dict={},
    word_dict=defaultdict(Counter)):
    ''' loop over list of documents to tokenize and update dicts
    '''
    docs = glob(os.path.join(path, '*.txt'))

    for doc in docs:
        tokenize_doc(doc, hashes=hashes, 
            sent_dict=sent_dict, word_dict=word_dict)
    return hashes, sent_dict, word_dict

if __name__ == '__main__':
    hashes, sent_dict, word_dict = tokenize_docs('test_docs')    

