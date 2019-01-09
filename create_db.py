'''
create_db.py

create db tables
'''

import sqlite3

def create_db(dbname):
    conn = sqlite3.connect(dbname)
    
    c = conn.cursor()
    
    # create table document
    c.execute('''CREATE TABLE document 
                (id INTEGER PRIMARY KEY,
                 document TEXT UNIQUE,
                 hash TEXT UNIQUE)
        ''')
    
    # create table sentence
    c.execute('''CREATE TABLE sentence
                (id INTEGER PRIMARY KEY,
                 sentence TEXT,
                 sentence_idx INTEGER,
                 document_id INTEGER,
                 FOREIGN KEY(document_id) REFERENCES document(id))
        ''')
                 
    # create table word
    c.execute('''CREATE TABLE word
                (id INTEGER PRIMARY KEY,
                 word TEXT UNIQUE)
        ''')
    
    # create table lemma
    c.execute('''CREATE TABLE lemma
                (id INTEGER PRIMARY KEY,
                 lemma TEXT UNIQUE)
        ''')
    
    # create table lemma_word_sentence
    c.execute('''CREATE TABLE lemma_word_sentence
                (lemma_id INTEGER,
                 word_id INTEGER,
                 sentence_id INTEGER,
                 count INTEGER,
                 FOREIGN KEY(lemma_id) REFERENCES lemma(id)
                 FOREIGN KEY(word_id) REFERENCES word(id)
                 FOREIGN KEY(sentence_id) REFERENCES sentence(id))
        ''')
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    from config import defaults
    create_db(defaults['DATABASE_NAME'])
