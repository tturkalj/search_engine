# -*- coding: utf-8 -*-
from __future__ import division
import sys
import os
import math
import resource
import re
from textblob import TextBlob
from timeit import default_timer
from shutil import copyfile


def main(argv):
    # search_term = argv[1]
    # print 'searching for word {0}'.format(search_term)
    start_time = default_timer()
    print u'start time {0}'.format(start_time)

    print u'start memory {0}'.format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)

    data_dir = '../../data/20news-bydate-train'
    # data_dir = 'data/small_train'

    document_number = 0
    term_in_doc_number = 0
    document_tf_dict = {}
    regex_pattern = re.compile(r"\b[a-z]+\b", re.IGNORECASE)

    document_words = {}

    print u'extracting words from documents...'
    for dir_path, dir_names, file_names in os.walk(data_dir):
        for file_name in file_names:
            file_path = os.path.join(dir_path, file_name)
            f = open(file_path, 'r')
            text = unicode(f.read(), 'ISO-8859-14')
            f.close()
            words = []
            reg = re.findall(regex_pattern, text)
            if reg:
                for x in reg:
                    words.append(x)
            document_words[file_name] = words


            # word_count = len(words)
            # search_term_count = words.count(search_term)
            # if search_term_count:
            #     document_tf = search_term_count / word_count
            #     document_words_data.append((file_path, words, document_tf))
            #     term_in_doc_number += 1
    extracting_words_timer = default_timer()

    print u'finished in {0} sec'.format(extracting_words_timer - start_time)

    print u'start indexing words...'
    document_word_tf_idf = {}
    for document in document_words:
        document_word_tf_idf[document] = {}
        words_list = document_words[document]
        for word in words_list:
            if word not in document_word_tf_idf[document]:
                word_in_doc_count = 0
                for temp in document_words:
                    if word in document_words[temp]:
                        word_in_doc_count += 1
                tf = words_list.count(word) / len(words_list)
                idf = math.log(len(document_words) / word_in_doc_count)
                document_word_tf_idf[document] = {word: tf * idf}

    indexing_words_timer = default_timer()
    print u'finished in {0} sec'.format(indexing_words_timer - start_time)

    # idf = math.log(document_number / (1 + term_in_doc_number))
    # tf_idf_doc_dict = {}
    # if document_tf_dict:
    #     for doc in document_tf_dict:
    #         tf_idf_doc_dict[doc] = document_tf_dict[doc] * idf
    #     sorted_doc_tf_idf = sorted(tf_idf_doc_dict.items(), key=lambda x: x[1])
    #     # for item in sorted_doc_tf_idf:
    #     #     print item

    print resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    end_time = default_timer()
    print u'time elapsed: {0}'.format(end_time - start_time)

if __name__ == '__main__':
    main(sys.argv)
