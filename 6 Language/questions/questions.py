import nltk
import sys
import string
import re
import collections
import os
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    filesdict = {}
    for f in os.listdir(directory):
        if f.endswith(".txt"):
            #fpath = os.path.join(directory, filename)
            with open(os.path.join(directory, f), encoding="utf8") as txtf:
               #print(f)
                contents = txtf.read()
                filesdict[f] = contents
    return filesdict
    raise NotImplementedError


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    tokens = nltk.word_tokenize(document.lower())
    #return [word  for word in tokens if re.search('[a-z]', word)]
    stopwords = nltk.corpus.stopwords.words("english")

    puncts_re =  "[" + string.punctuation + "]"
    return [word  for word in tokens if not re.search(puncts_re, word) and word not in stopwords ]

    raise NotImplementedError


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """

    word_idf = {}
    for doc in documents:
       #print(doc)
        wordindoc = {}
        for word in documents[doc]:
           #print(word)
            if word not in wordindoc:
                wordindoc[word]=1 #does document contain word

        for word in wordindoc: #NumDocumentsContaining(word)
            if word in word_idf:
                word_idf[word]+=1
            else:
                word_idf[word]=1
    #print(word_idf,"word idf")
    numofdocs = len(documents)
    for word in word_idf:
        word_idf[word] = math.log((numofdocs / word_idf[word]))
    #print(word_idf)
    return word_idf

    raise NotImplementedError


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    filescores = {}
    for f in files:
        sum_tf=0
        wordcount = collections.Counter(files[f])
        for word in query:
            if word in wordcount:
                tf = wordcount[word] #number of times word appears in file
                #print(idfs)
                tfidf = tf*idfs[word]
                sum_tf += tfidf
        filescores[f] = sum_tf
    sortedscores = sorted(filescores.keys(), key = lambda x:filescores[x],reverse = True)    
    #print(sortedscores[0:n],"soreted")
    return sortedscores[0:n]

    raise NotImplementedError


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    scores = {}
    
    qtdensity ={}
    for s in sentences:
        #sum_idf = sum((idfs[word] for word in query if word in sentences[s]))
        qt_count = 0
        sum_idf =0
        for word in query:
            if word in sentences[s]:
                qt_count +=1
                sum_idf += idfs[word]
            qtdensity[s] = qt_count/len(sentences[s]) #len of list of words
            scores[s] = sum_idf
    #print(scores,"scores sentence")
    sortedscores = sorted(scores.keys(), key = lambda x: (scores[x] , qtdensity[x]) ,reverse = True)    

    """
    sorting for qtdensity would be more efficient only if ties occur, but rather troublesome
    qtdensity = {}
    numties = 0
    if n< len(scores): #check for ties
    tie_idf = scores[sortedscores[n]]
        if tie_idf == scores[sortedscores[n+1]]:
                for doc, value in scores.items():
                    if tie_idf == value:
                        numties +=1
                        """
    #print(sortedscores[0:n],"sorted sentecnes")
    return sortedscores[0:n]
    raise NotImplementedError


if __name__ == "__main__":
    main()
