import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import *
from collections import defaultdict
import shelve

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()


class CorpusProcess:
    def __init__(self, corpus):

        dict_set = defaultdict(set)
        dict_list = defaultdict(list)

        db = shelve.open('shelveDict')
        stop_words = set(stopwords.words('english'))
        db['stopwords'] = stop_words
        db.close()
        for movie_id in corpus.keys():
            # print "movie_id is " + movie_id
            normalized_words = self.normalization(corpus[movie_id]["text"])[0]
            for w in normalized_words:
                dict_set[w].add(movie_id)

        for w in dict_set.keys():
            tmplist = list(dict_set[w])
            tmplist.sort(self.my_comparator)
            dict_list[w] = tmplist

        db = shelve.open('shelveDict')

        db['dict_w_list'] = dict_list

        db.close()

    def normalization(self, text):
        res = []
        stpw_query = []
        db = shelve.open('shelveDict')
        stop_words = db['stopwords']

        word_tokens = word_tokenize(text)

        for i in range(len(word_tokens)):
            w = str(word_tokens[i])

            if w not in stop_words:
                w = lemmatizer.lemmatize(w)
                w = stemmer.stem(w)

                res.append(w)
            else:
                stpw_query.append(w)

        return [res, stpw_query]

    def search(self, query):
        res = []
        normalized_res = self.normalization(query)
        normalized_queries = normalized_res[0]

        stpw_query = normalized_res[1]
        unknown_words = []

        db = shelve.open('shelveDict')
        dict_list = db['dict_w_list']
        i = 0
        while i < len(normalized_queries) and normalized_queries[i] not in dict_list:
            unknown_words.append(normalized_queries[i])
            i += 1

        if i < len(normalized_queries):
            res = dict_list[normalized_queries[i]]
            i += 1

        for j in range(i, len(normalized_queries)):
            token = normalized_queries[j]
            if token in dict_list:
                res = self.intersect(res, dict_list[token])
            else:
                unknown_words.append(token)

        return [res, stpw_query, unknown_words]

    def intersect(self, list1, list2):
        print "list1 is " + str(list1)
        print "list2 is " + str(list2)
        i = 0
        j = 0
        res = []
        while i < len(list1) and j < len(list2):

            num1 = int(list1[i])
            num2 = int(list2[j])

            if num1 < num2:
                i += 1
            elif num1 > num2:
                j += 1
            else:
                res.append(list1[i])
                i += 1
                j += 1

        return res

    def my_comparator(self, x, y):
        num1 = int(x)
        num2 = int(y)
        return num1 - num2
