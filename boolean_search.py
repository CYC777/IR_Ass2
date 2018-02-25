# -*- coding: utf-8 -*-
import json
import shelve
"""
boolean_search.py
author: 

Students: Modify this file to include functions that implement 
Boolean search, snippet generation, and doc_data presentation.
"""


def readJson():
    json1_file = open('test_corpus.json')
    json1_str = json1_file.read()
    corpus= json.loads(json1_str)
    db = shelve.open('shelveDict')
    db['corpus'] = corpus
    db.close()



def dummy_movie_data(doc_id, corpus):
    """
    Return data fields for a movie.
    Your code should use the doc_id as the key to access the shelf entry for the movie doc_data.
    You can decide which fields to display, but include at least title and text.
    """

    return corpus[doc_id]


def dummy_movie_snippet(doc_id, corpus):
        """
        Return a snippet for the results page.
        Needs to include a title and a short description.
        Your snippet does not have to include any query terms, but you may want to think about implementing
        that feature. Consider the effect of normalization of index terms (e.g., stemming), which will affect
        the ease of matching query terms to words in the text.
        """
        doc_id = str(doc_id)

        title = ""
        text = ""
        try:
            title = corpus[doc_id]["title"]
        except:
            print "title failed"
        try:
            text = corpus[doc_id]["text"]
        except:
            print "text failed"
        return (doc_id, title, text)


