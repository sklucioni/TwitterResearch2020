#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 14 13:50:33 2020

@author: jimwaldo

Turns the tweets gathered in lots of files into a single file, stored as the pickle of a list of thinned_tweet objects.
While doing this, the program also creates a dictionary keyed by tweeter ID with value the number of tweets posted on
that day.
"""

import os, json, sys, time
import thinned_tweet_obj as tt
from general_utilities import write_pkl

def build_file_list(d_pattern, f_pattern):
    dir_list = os.listdir('.')
    return_l = []
    for d in dir_list:
        if d_pattern in d and os.path.isdir(d):
            all_files = os.listdir(d)
            for f in all_files:
                if f_pattern in f:
                    return_l.append('/'.join([d, f]))
    return return_l

def build_dir_list(start_d, end_d):
    return_l = []
    all_d = os.listdir('.')
    for d in all_d:
        if '20' in d and start_d <= d and d <= end_d:
            return_l.append(d)
    return return_l

def add_to_list(f_name, id_set, thin_l, user_d):
    fin = open(f_name, 'r')
    j_l = json.load(fin)
    fin.close()
    
    for t in j_l:
        if t['id_str'] in id_set:
            continue
        thin_l.append(tt.tweet(t))
        id_set.add(t['id_str'])
        user_d[t['user']['id_str']] = user_d.setdefault(t['user']['id_str'])
    return None

def process_day_files(t_day, file_l):
    print('Processing day ' + t_day)
    start_t = time.time()
    user_d = {}
    thin_l = []
    id_s = set()
    for f in file_l:
        add_to_list(f, id_s, thin_l, user_d)
    write_pkl('.'.join([t_day, '.pkl']), thin_l)
    write_pkl(''.join([t_day, 'id_post_d.pkl']), user_d)
    end_t = time.time()
    print('elapsed time for ', t_day, 'is', end_t - start_t)
    return None
        
    

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: python thin_and_merge.py start_date end_date')
        sys.exit(1)

    start_d = sys.argv[1]
    end_d = sys.argv[2]
    print (start_d, end_d)
    if start_d > end_d:
        print('Usage: python thin_and_merge.py start_date end_date')
        print('Start date must not be after end date')
        sys.exit(1)
        
    dir_l = build_dir_list(start_d, end_d)
    dir_s = set()
    for d in dir_l:
        day = d[:10]
        if day not in dir_s:
            dir_s.add(day)
            f_l = build_file_list(day, 'json')
            process_day_files(day, f_l)