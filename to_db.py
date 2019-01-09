#!/usr/bin/env python3

'''
to_db.py

update db with tokenized text
'''

import os
from glob import glob
from time import time
import pandas as pd
import update_db as udb
from tokenize_docs import tokenize_docs
from config import defaults

db = defaults['DATABASE_NAME']

def update_document_table(hashes):
    '''preprocess and insert document table rows'''
    check_names = udb.check_document_name(list(hashes))
    print(check_names)
    if len(check_names) > 0:
        print('''The following document names are already in the database,
                please remove these documents from the document list
                for processing.''')
        print(list(zip(*check_names))[0])
        return
    hashes_inverted = {
        doc_hash: doc_name for doc_name, doc_hash in hashes.items()}
    check_hashes = udb.check_document_hash(list(hashes_inverted))
    # returns and stops execution if doc_name already in db
    if len(check_hashes) > 0:
        print('''The following documents are already in the database,
                please remove these documents from the document list
                for processing.''')
        print(list(zip(*check_hashes))[0])
        return
    
    udb.insert_rows('document',list(hashes.items()), 'document', 'hash')
    return True

def update_sentence_table(sent_dict):
    '''preprocess and insert sentence table rows'''
    for doc_name in sent_dict:
        sents = sent_dict[doc_name]
        doc_id = udb.check_col_val('document', 'id', 'document', doc_name)[0][0]
        sents = [(sents[i], i, doc_id) for i in range(len(sents))]
        udb.insert_rows('sentence', sents, 
            'sentence', 'sentence_idx', 'document_id')

def word_dict_to_df(word_dict):
    '''convert word_dict to a df
    '''
    df_list = []
    for k in word_dict:
        df = pd.DataFrame.from_dict(
            word_dict[k], orient='index', columns=['count'])
        df['word'] = k[0]
        df['lemma'] = k[1]
        df_list.append(df)
    word_lemma_df = pd.concat(df_list)
    word_lemma_df.index = pd.MultiIndex.from_tuples(word_lemma_df.index)
    word_lemma_df.index.names=['doc_name', 'sent_idx']
    word_lemma_df.reset_index(inplace=True)

    return word_lemma_df

def update_word_table(word_lemma_df):
    ''' insert rows into word table
    '''
    new_words = [(word,) for word in word_lemma_df['word']]
    udb.check_update_word_table(new_words)

def update_lemma_table(word_lemma_df):
    ''' insert rows into lemma table
    '''
    new_lemmas = [(lemma,) for lemma in word_lemma_df['lemma']]
    udb.check_update_lemma_table(new_lemmas)

def update_lemma_word_sentence_table(word_lemma_df):
    ''' insert rows into lemma_word_sentence table
    '''
    word_lemma_df = word_lemma_df[
        ['lemma', 'word', 'doc_name', 'sent_idx', 'count']]
    wordlemma_docname_sentidx_count =\
        word_lemma_df.itertuples(index=False, name=None)
    udb.check_update_lemma_word_sentence_table(wordlemma_docname_sentidx_count)
    
def process_to_db(hashes, sent_dict, word_dict):
    ''' update all tables with tokenized text
    '''
    docs_test = update_document_table(hashes)
    if not docs_test:
        return
    update_sentence_table(sent_dict)
    word_lemma_df = word_dict_to_df(word_dict)
    update_word_table(word_lemma_df)
    update_lemma_table(word_lemma_df)
    #words_lemmas_df = update_word_table(word_dict)
    update_lemma_word_sentence_table(word_lemma_df)

def update_db(path, dbname=db):
    '''ingest text files - tokenize - process to db
    '''
    hashes, sent_dict, word_dict = tokenize_docs(path)
    process_to_db(hashes, sent_dict, word_dict)

if __name__ == '__main__':
    path = 'test_docs'
    t = time()
    process_to_db(path)
    print(time() -t)
