'''
update_db.py

functions to update table rows with tokenized text
'''

import sqlite3
from config import defaults

db = defaults['DATABASE_NAME']

def check_col_val(table, query, col, val, dbname=db):
    '''select query from table if col=val
    '''
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    c.execute('''SELECT %s FROM %s
                 WHERE %s=?
              ''' % (query, table, col), (val,))

    result = c.fetchall()
    conn.close()
    return result

def get_cols(table, *cols, dbname=db):
    '''select col from table
    '''
    dbname = dbname+'.db'
    conn = sqlite3.connect(db)
    c = conn.cursor()

    c.execute('''SELECT %s FROM %s
              ''' % (','.join(cols),table))

    result = c.fetchall()
    conn.close()
    return result

def insert_rows(table, rows, *cols, dbname=db):
    '''insert list of rows into table
    '''
    dbname = dbname+'.db'
    conn = sqlite3.connect(db)
    c = conn.cursor()
    l = len(cols)
    c.executemany('''INSERT INTO %s
                     (%s)
                     VALUES
                     (%s)
                  ''' % (table , ','.join(cols), ','.join('?'*l)), (rows))

    conn.commit()
    conn.close()

def check_update_word_table(words, dbname=db):
    '''check if word in words exists in db - and insert if not
    '''
    dbname = dbname+'.db'
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('''CREATE TEMP TABLE word_vals
                (word)''')
    c.executemany('''INSERT INTO word_vals
                    (word)
                    VALUES(?)''',(words))
    conn.commit()
    c.execute('''SELECT word FROM word w
                WHERE w.word IN
                (SELECT word FROM word_vals)''')
    result = c.fetchall()            
   
    c.executemany('''INSERT INTO word
                     (word)
                     VALUES
                     (?)''',list(set(words)-set(result)))
    conn.commit()
    conn.close()

def check_update_lemma_table(lemmas, dbname=db):
    '''check if lemma in lemmas exists in db - and insert if not
    '''
    dbname = dbname+'.db'
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('''CREATE TEMP TABLE lemma_vals
                (lemma)''')
    c.executemany('''INSERT INTO lemma_vals
                    (lemma)
                    VALUES(?)''',(lemmas))
    conn.commit()
    c.execute('''SELECT lemma FROM lemma l
                WHERE l.lemma IN
                (SELECT lemma FROM lemma_vals)''')
    result = c.fetchall()            
   
    c.executemany('''INSERT INTO lemma
                     (lemma)
                     VALUES
                     (?)''',list(set(lemmas)-set(result)))
    conn.commit()
    conn.close()

def check_update_lemma_word_sentence_table(
        lemmaword_docname_sentidx_count, dbname=db):
    '''get word and lemma pl id and insert lemma-word-sntence
    into lemma_word_sentence table
    '''
    dbname = dbname+'.db'
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('''CREATE TEMP TABLE lwdsc
                (lemma, word, doc, senidx, count)''')
    c.executemany('''INSERT INTO lwdsc
                    (lemma, word, doc, senidx, count)
                    VALUES(?,?,?,?,?)''', lemmaword_docname_sentidx_count)
    conn.commit()
    
    c.execute('''SELECT l.id, w.id, a.id, lwdsc.count 
                FROM lwdsc
                LEFT JOIN word w
                ON w.word=lwdsc.word
                LEFT JOIN lemma l
                ON l.lemma=lwdsc.lemma
                LEFT JOIN
                (SELECT s.id, d.document, s.sentence_idx
                FROM sentence s
                JOIN document d
                ON d.id=s.document_id) a
                WHERE lwdsc.doc=a.document
                AND lwdsc.senidx=a.sentence_idx
                ''')
    result = c.fetchall()            
    print(len(result))   
    c.executemany('''INSERT INTO lemma_word_sentence
                     (lemma_id, word_id, sentence_id, count)
                     VALUES
                     (?,?,?,?)
                  ''', result)
    conn.commit()
    conn.close()

def check_document_name(names, dbname=db):
    '''check if a hash exists in document table
    '''
    dbname = dbname+'.db'
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('''SELECT document FROM document
                 WHERE document IN (%s)
              ''' % ','.join('?'*len(names)), names)
    
    result = c.fetchall()
    conn.close()
    return result

def check_document_hash(hashes, dbname=db):
    '''check if a hash exists in document table
    '''
    dbname = dbname+'.db'
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('''SELECT hash FROM document
                 WHERE hash IN (%s)
              ''' % ','.join('?'*len(hashes)), hashes)
    
    result = c.fetchall()
    conn.close()
    return result

