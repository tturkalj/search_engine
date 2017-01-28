# -*- coding: utf-8 -*-
from __future__ import division
import sys
import os
import math
import resource
import re
import sys
from timeit import default_timer
from shutil import copyfile
from array import array

start_time = default_timer()


def get_elapsed_time():
    return default_timer() - start_time


def main(argv):
    search_term = argv[1]
    print u'searching for word {0}'.format(search_term)

    print u'start time {0}'.format(start_time)

    print u'start memory {0}'.format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)

    data_dir = '../../data/20news-bydate-test'
    # data_dir = 'data/small_train'

    regex_pattern = re.compile(r"\b[a-z]+\b", re.IGNORECASE)

    document_words = []

    print u'extracting words from documents...'
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
        print u'folder {0} finished'.format(dir_path)

    print u'finished in {0} sec'.format(get_elapsed_time())
    
    print u'start indexing words in {0} document'.format(len(document_words))
    document_word_tf_idf = {}
    for document, words in document_words:
        document_word_tf_idf[document] = {}
        for word in words:
            if word not in document_word_tf_idf[document]:
                word_in_doc_count = 1
                for temp_doc, temp_words in document_words:
                    if temp_doc != document and word in temp_words:
                        word_in_doc_count += 1
                tf = words.count(word) / len(words)
                idf = math.log(len(document_words) / word_in_doc_count)
                document_word_tf_idf[document].update({word: tf * idf})

    print u'finished in {0} sec'.format(get_elapsed_time())

    print u'Document order for word {0}:'.format(search_term)
    results = document_word_tf_idf.get(search_term, None)
    if results:
        print sorted(results.items(), key=lambda x: x[1])
    else:
        print u'Term no found'

    print u'time elapsed: {0}'.format(get_elapsed_time())

if __name__ == '__main__':
    main(sys.argv)
