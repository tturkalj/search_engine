# -*- coding: utf-8 -*-
from __future__ import division
import os
import math
import re
import sys
from timeit import default_timer
import argparse

start_time = default_timer()


def get_elapsed_time():
    return default_timer() - start_time


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-data_dir', action='store', help='path to directory with documents')
    parser.add_argument('-search_term', action='store', nargs='+', help='search term')

    args = parser.parse_args()

    regex_pattern = re.compile(r"\b[a-z]+\b", re.IGNORECASE)

    print u'Extracting words from documents...'
    document_words = []
    for dir_path, dir_names, file_names in os.walk(args.data_dir):
        for file_name in file_names:
            #read file with given encoding
            file_path = os.path.join(dir_path, file_name)
            with open(file_path, 'r') as f:
                text = unicode(f.read(), encoding='ISO-8859-14')

            #parse text with given regex pattern
            words = []
            reg = re.findall(regex_pattern, text)
            if reg:
                for x in reg:
                    if x:
                        words.append(x)
            if words:
                document_words.append((file_name, words))
    print u'finished in {0} sec'.format(get_elapsed_time())

    print u'Start indexing words in {0} documents...'.format(len(document_words))
    document_word_tf_idf = {}

    #total number of documents
    document_count = len(document_words)

    for document, words in document_words:
        for word in words:
            #number of documents that contain word
            word_in_doc_count = 1
            for temp_doc, temp_words in document_words:
                if temp_doc != document and word in temp_words:
                    word_in_doc_count += 1

            #calculate tf-idf for word
            tf = words.count(word) / len(words)
            idf = math.log(document_count / word_in_doc_count)
            tfidf = tf * idf
            if word in document_word_tf_idf:
                old_dict = document_word_tf_idf[word]
                if document not in old_dict:
                    old_dict.update({document: tfidf})
                    document_word_tf_idf[word] = old_dict
            else:
                document_word_tf_idf[word] = {document: tfidf}

    print u'finished in {0} sec'.format(get_elapsed_time())

    print u'Document order for search term: {0}'.format(u' '.join(args.search_term))

    #get document order for search term
    result_dict = {}
    for word in args.search_term:
        if word in document_word_tf_idf:
            results = document_word_tf_idf.get(word, None)
            if results:
                for doc, tfidf in results.items():
                    #add tf-idf for each word in search term
                    if doc in result_dict:
                        result_dict[doc] = result_dict[doc] + tfidf
                    else:
                        result_dict[doc] = tfidf

    #sort results
    if result_dict:
        sorted_results = sorted(result_dict.items(), key=lambda x: x[1])
        for item in sorted_results:
            print item
    else:
        print u'Search term not found'


if __name__ == '__main__':
    main(sys.argv)
