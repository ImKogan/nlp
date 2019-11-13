# NLP text analyzer

CLI that ingests documents, tokenizes the text using nltk, and uploads
to a SQLite databse. A report with summary statistics, such as frequency,
location and lemmas can be generated from the db.

## Getting Started
### Prerequisites
All you need is the standard python3 library and pip3.
Here is the official link to check wether you have pip3, and how to install it
[Install pip](https://packaging.python.org/tutorials/installing-packages/#ensure-you-can-run-pip-from-the-command-line)
(You can do without pip - and use another package manager, as long as the required packages are downloaded.)

### Installing

The most straightforward way to get up and running:

cd into project directory
```bash
python3 -m venv <env_name>
```

activate the virtual env
```bash
source <env_name>/bin/activate
```

install the required packages
```bash
pip3 install -r requirements.txt
```

create a database
```bash
python3 run.py createdb
```

project is ready for use!

To process some text files, first make sure that the directory
the files are in, don't contain .txt files you do not wish to process.
then in shell:
```bash
python3 run.py updatedb --path <path to files directory>
```

Now to get a report of 10 most common words in the processed files:
```bash
python3 run.py report
```

You will get a report of the top 10 occuring words in you browser
There are many options that can be supplied to the commands
such as name of db, file to save to, top n words, see lemmas and so on.
Check out the options for each command by running run.py command -h

Note that if you just run run.py without supplying any arguments, no error will be thrown, but nothing will happen. There is an issue with argparse in python3 - so I left it like this.
[argparse bug](https://bugs.python.org/issue29298)

## Some Notes and Justification of Design
### Database
The choice to include a database in the pipeline was based on the
extensibility consideration. It is certainly possible to do a one-of
processing without a db, but it is not a viable solution - it is also
the natural way to store the data.
On the other hand, I didn't make a full fledged db, satisfying myself with
SQLite as a full db would be out of scope for this project.

### Algorithms used
As I'm new to the nltk package, I limited myself to lemmatization.
I did look into proper noun tagging for example, but didn't include in the processing.

### Assumptions
Every document is hashed and hash stored in document table. At ingestion,
each document's hash is checked against the database. If any document's
hash matches an existing hash in the db, the process is aborted.
Correspondingly, document names are also maintained as unique, so
a duplicate name isn't allowed either. 

### Implementation
The database has the following tables:
* document
* sentence
* word
* lemma
* lemma_word_sentence

The last one is triple relationship table between lemma, word, sentence.
In other words, every record in lemma_word_sentence sorresponds to a
unique (lemma,word) combination in a sentence. This allows filtering
in all possile ways, unique qord-sentence, lemma-sentence, or lemma-sentence-word combinations. 

### Improvement
I also wanted to include version control - (most likely a version column in each table, so the same text can be stored in the db if processed using a changed processing implementation). 
