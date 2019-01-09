'''
report.py

generate reports from db
'''

import os
import webbrowser
import sqlite3
import pandas as pd
from config import defaults

pd.set_option('display.max_colwidth', -1)
db = defaults['DATABASE_NAME']

conn = sqlite3.connect(db)

def report(filename, limit, lemmas, dbname=db,
    documents=None, most=True, display_format='html'):
    '''generate report and save to file
    '''
    if lemmas:
        print('lemmas')
    direction =''
    if most:
        direction = 'DESC'

    if not lemmas:
        sql='''SELECT s.sentence, d.document, w.word
        FROM lemma_word_sentence lws
        LEFT JOIN sentence s
        ON s.id=lws.sentence_id
        LEFT JOIN document d 
        ON d.id=s.document_id
        LEFT JOIN word w 
        ON w.id=lws.word_id
        
        LEFT JOIN 
        (SELECT w.id , w.word
        FROM word w 
        JOIN lemma_word_sentence lws
        ON w.id=lws.word_id
        GROUP BY w.id
        ORDER BY
        SUM(lws.count) {}
        LIMIT {}) ranking
        ON lws.word_id=ranking.id
        WHERE ranking.id IS NOT NULL
        ORDER BY w.word, d.document, s.sentence {}
        '''.format(direction, limit, direction)

    else:
        sql='''SELECT s.sentence, d.document, l.lemma
        FROM lemma_word_sentence lws
        LEFT JOIN sentence s
        ON s.id=lws.sentence_id
        LEFT JOIN document d 
        ON d.id=s.document_id
        LEFT JOIN lemma l
        ON l.id=lws.lemma_id
        
        LEFT JOIN 
        (SELECT l.id , l.lemma
        FROM lemma l
        JOIN lemma_word_sentence lws
        ON l.id=lws.lemma_id
        GROUP BY l.id
        ORDER BY
        SUM(lws.count) {}
        LIMIT {}) ranking
        ON lws.lemma_id=ranking.id
        WHERE ranking.id IS NOT NULL
        ORDER BY l.lemma, d.document, s.sentence {}
        '''.format(direction, limit, direction)
    
    
    df = pd.read_sql_query(sql,conn)
    if documents:
        df.set_index('document', drop=False, inplace=True)
        df = df[df.index.isin(documents)]
    if not lemmas:
        df['count'] = df['word'].groupby(
            df['word']).transform('count')
        df.sort_values(by=['count', 'word', 'document'],
            ascending=[False, True, True], inplace=True)
        df = df[['word', 'document', 'sentence', 'count']]
    else:
        df['count'] = df['lemma'].groupby(
            df['lemma']).transform('count')
        df.sort_values(by=['count', 'lemma', 'document'],
            ascending=[False, True, True], inplace=True)
        df = df[['lemma', 'document', 'sentence', 'count']]
    print(df.shape)
    #quit()
    if display_format=='html':
        df.to_html(open(filename+'.html', 'w'), index=False)
        webbrowser.open('file://' + os.path.realpath(filename+'.html'))
    elif display_format=='csv':
        df.to_csv(filename+'.csv', index=False)
       
if __name__ == '__main__':
    pass
