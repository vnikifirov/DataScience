#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os.path


# fix it and add main() func
# fix path and cheking the way to save file
# if path is not specify, nltk will download files by automate mode in default folder


# how can I looking for standart default folder for nltk

def setup(path = os.path.abspath(input("Enter path to download nltk,or press enter and path to folder will be default: "))):
    try:
        os.makedirs(path)
    except OSError:
        if not os.path.isfile(path):
            print("nltk not exist and will be download")
            raise

            nltk.download('nltk')

setup(path)

# if module file is exist -> break
# else:
#    input() or default path

# if len of path == 0, then we need to download nltk and other requiremtns?

def find(name, path):
    for root, dirs, files in scandir.walk(path):
        if root.endswith(name):
            return root

def find_nltk_data():
    start = time.time()
    path_to_nltk_data = find('nltk_data', '/')
    print >> sys.stderr, 'Finding nltk_data took', time.time() - start
    print >> sys.stderr,  'nltk_data at', path_to_nltk_data
    with open('where_is_nltk_data.txt', 'w') as fout:
        fout.write(path_to_nltk_data)
    return path_to_nltk_data

def magically_find_nltk_data():
    if os.path.exists('where_is_nltk_data.txt'):
        with open('where_is_nltk_data.txt') as fin:
            path_to_nltk_data = fin.read().strip()
        if os.path.exists(path_to_nltk_data):
            nltk.data.path.append(path_to_nltk_data)
        else:
            nltk.data.path.append(find_nltk_data())
    else:
        path_to_nltk_data  = find_nltk_data()
        nltk.data.path.append(path_to_nltk_data)


magically_find_nltk_data()
print nltk.pos_tag('this is a foo bar'.split())
