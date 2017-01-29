# -*- coding: utf-8 -*-
from __future__ import division
import sys
import os
import math
import resource
import re
import sys
from timeit import default_timer
from sklearn.feature_extraction.text import TfidfVectorizer
start_time = default_timer()


def get_elapsed_time():
    return default_timer() - start_time


def main(argv):
    search_term = argv[1]
    data_dir = '../../data/20news-bydate-test'
    # data_dir = 'data/small_train'

    regex_pattern = re.compile(r"\b[a-z]+\b", re.IGNORECASE)

    print u'Extracting words from documents...',
    document_words = []
    for dir_path, dir_names, file_names in os.walk(data_dir):
        for file_name in file_names:
            file_path = os.path.join(dir_path, file_name)
            with open(file_path, 'r') as f:
                text = unicode(f.read(), 'ISO-8859-14')

            words = []
            reg = re.findall(regex_pattern, text)
            if reg:
                for x in reg:
                    words.append(x)
            document_words.append((file_name, words))
    print u'finished in {0} sec'.format(get_elapsed_time())

    print u'Start indexing words in {0} documents...'.format(len(document_words)),
    document_word_tf_idf = {}
    document_words_len = len(document_words)
    for document, words in document_words:
        for word in words:
            word_in_doc_count = 1
            for temp_doc, temp_words in document_words:
                if temp_doc != document and word in temp_words:
                    word_in_doc_count += 1
            if word not in document_word_tf_idf:
                document_word_tf_idf[word] = (word_in_doc_count, {})

            tf = words.count(word) / len(words)
            idf = math.log(document_words_len / document_word_tf_idf[word][0])
            document_word_tf_idf[word][1].update({document: tf * idf})

    print u'finished in {0} sec'.format(get_elapsed_time())

    print u'Document order for search term: {0}'.format(search_term)

    result_dict = {}
    for word in search_term:
        results = document_word_tf_idf[word].get(search_term, None)
        if results:
            for doc, tfidf in results:
                if doc in result_dict:
                    result_dict[doc] = result_dict[doc] + tfidf
                else:
                    result_dict[doc] = tfidf

    if result_dict:
        sorted_results = sorted(result_dict[1].items(), key=lambda x: x[1])
        print sorted_results
    else:
        print u'Search term not found'

    print u'Time elapsed: {0}'.format(get_elapsed_time())

if __name__ == '__main__':
    main(sys.argv)
