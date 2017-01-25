# -*- coding: utf-8 -*-
from __future__ import division
import sys
import os
import math
import resource
import re
from textblob import TextBlob
from timeit import default_timer


def main(argv):
    search_term = argv[1]
    print 'searching for word {0}'.format(search_term)
    start_time = default_timer()
    print resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    data_dir = 'data/20news-bydate-train'
    # data_dir = 'data/small_train'

    document_number = 0
    term_in_doc_number = 0
    document_tf_dict = {}

    for dir_path, dir_names, file_names in os.walk(data_dir):
        for file_name in file_names:
            file_path = os.path.join(dir_path, file_name)
            with open(file_path, 'r') as f:
                document_number += 1
                text = unicode(f.read(), 'ISO-8859-14')
                # blob = TextBlob(text)
                # blob_word_count = len(blob.words)
                # print blob.words
                words = []
                for word in text.split():
                    reg = re.findall(r"\b[a-z]+\b", word, re.IGNORECASE)
                    if reg:
                        for x in reg:
                            words.append(x)
                # print words
                word_count = len(words)
                # print words
                # print u'Document {0} -> TextBlob word count: {1}, Regex word count {2}'.format(
                #     file_path, blob_word_count, word_count
                # )
                # print 'word count {0}'.format(word_count)
                if word_count:
                    # blob_term_count = blob.words.count(search_term)
                    term_count = words.count(search_term)
                    # print u'Document {0} -> TextBlob term count: {1}, Regex term count {2}'.format(
                    #     file_path, blob_term_count, term_count
                    # )
                    # print 'term_count count {0}'.format(term_count)
                    if term_count:
                        document_tf = term_count / word_count
                        document_tf_dict[file_path] = document_tf
                        term_in_doc_number += 1

    # print u'idf without log {0}'.format(document_number / (1 + term_in_doc_number))
    idf = math.log(document_number / (1 + term_in_doc_number))
    # print u'idf with log {0}'.format(idf)
    print document_tf_dict
    tf_idf_doc_dict = {}
    if document_tf_dict:
        for doc in document_tf_dict:
            tf_idf_doc_dict[doc] = document_tf_dict[doc] * idf
        sorted_doc_tf_idf = sorted(tf_idf_doc_dict.items(), key=lambda x: x[1])
        for item in sorted_doc_tf_idf:
            print item

    print resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    end_time = default_timer()
    print u'time elapsed: {0}'.format(end_time - start_time)

if __name__ == '__main__':
    main(sys.argv)
