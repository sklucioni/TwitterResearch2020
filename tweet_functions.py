#!/usr/bin/env python
# coding: utf-8

"""
Created on 11/20/2020

@author dashamet

Functions to load tweets from the drive, find tweets containing certain key words, and calculate various stats
"""

import datetime
import statistics
import gdrive_quickstart
import general_utilities
import thinned_tweet_obj
import re
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns 
import random
import csv
# Make sure you have API credentials for this authentication to work
DRIVE = gdrive_quickstart.authenticate_drive_api()

def load_tweets(start_date, end_date):
    '''
    takes in start and end date: both strings, use 'year-month-day' format (e.g. '2020-09-25')
    returns dict of tweet objects for each date within range (inclusive of start and end date)
    '''
    sdate = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
    edate = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
    delta = edate - sdate       
    loaded_tweets = {}
    for i in range(delta.days + 1):
        day = str(sdate + datetime.timedelta(days=i))
        file_name = 'combined_tweets-' + str(day)
        file_obj = gdrive_quickstart.get_file_objs_list(DRIVE, "name contains '{}'".format(file_name))[0]
        loaded_tweets[day] = gdrive_quickstart.download_pkl_file(DRIVE, file_obj, print_status=True)
    return loaded_tweets


def find_tweets(tweets_list, words_list):
    '''
    run load_tweets function prior to running this function
    takes in tweets: variable name for a list of tweets (whatever stores the results of load_tweets)
    takes in words_list: a list of strings to search tweets for
    returns dict of tweets objects that contain any of input strings for each date in dict returned by load_tweets
    '''
    search_words = '|'.join(words_list)
    filtered_tweets_list = {}
    for day in tweets_list.keys():
        filtered_tweets = []
        for tweet in tweets_list[day]:
            if tweet.retweet != '':
                if bool(re.search(search_words, tweet.retweet.text, re.IGNORECASE)):
                    filtered_tweets.append(tweet)
            else:
                if bool(re.search(search_words, tweet.text, re.IGNORECASE)):
                    filtered_tweets.append(tweet)
        filtered_tweets_list[day] = filtered_tweets
    return filtered_tweets_list

def calc_tweets(filtered_tweets, calc, unfiltered_tweets=None):
    '''
    run load_tweets and find_tweets prior to running this function 
    takes in filtered_tweets, the name of a list of filtered tweets (whatever variable stores results of find_tweets)
    takes in unfiltered_tweets, the name of a list of unfiltered tweets (whatever variable stores results of load_tweets)
        note that unfiltered_tweets only needs to be specified for calc = 'prop_tweets'
    takes in calculation type (string), which is one of the following:
        'count_tweets' = number of tweets
        'prop_tweets' = proportion of tweets out of all scraped that day
        'count_retweets' = number of retweets
        'prop_retweets' = proportion of retweets out of all filtered tweets that day
        'count_replies' = number of replies
        'prop_replies' = proportion of replies out of all filtered tweets that day
        'count_users' = number of unique users
        'avg_tweets_per_user' = average number of tweets per unique user
        'avg_followers_per_user' = average number of followers per unique user
        'avg_favorite_count' = average number of favorites per tweet (only counts retweets)
        'retweets_and_likes_to_replies' = median ratio of retweets and likes to replies 
    returns dictionary with results of calculation for each date in dict returned by find_tweets
    '''
    results = {}
    
    if calc == 'count_tweets':
        for day in filtered_tweets.keys():
            results[day] = len(filtered_tweets[day])
    
    if calc == 'prop_tweets':
        for day in filtered_tweets.keys():
            results[day] = len(filtered_tweets[day])/len(unfiltered_tweets[day])
            
    if calc == 'count_retweets':
        for day in filtered_tweets.keys():
            retweets = 0
            for tweet in filtered_tweets[day]:
                if bool(re.search('^RT @', tweet.text)):
                    retweets += 1
            results[day] = retweets
    
    if calc == 'prop_retweets':
        for day in filtered_tweets.keys():
            retweets = 0
            for tweet in filtered_tweets[day]:
                if bool(re.search('^RT @', tweet.text)):
                    retweets += 1
            results[day] = retweets/len(filtered_tweets[day])
            
    if calc == 'count_replies':
        for day in filtered_tweets.keys():
            replies = 0
            for tweet in filtered_tweets[day]:
                if tweet.is_reply():
                    replies += 1
            results[day] = replies
    
    if calc == 'prop_replies':
        for day in filtered_tweets.keys():
            replies = 0
            for tweet in filtered_tweets[day]:
                if tweet.is_reply():
                    replies += 1
            results[day] = replies/len(filtered_tweets[day])
    
    if calc == 'count_users':
        for day in filtered_tweets.keys():
            unique_users = []
            users = 0
            for tweet in filtered_tweets[day]:
                user_id = tweet.get_user_id()
                if user_id not in unique_users:
                    unique_users.append(user_id)
                    users += 1
            results[day] = users
    
    if calc == 'avg_tweets_per_user':
        for day in filtered_tweets.keys():
            unique_users = []
            users = 0
            for tweet in filtered_tweets[day]:
                user_id = tweet.get_user_id()
                if user_id not in unique_users:
                    unique_users.append(user_id)
                    users += 1
            results[day] = len(filtered_tweets[day])/users
    
    if calc == 'avg_followers_per_user':
        for day in filtered_tweets.keys():
            unique_users = []
            followers = []
            users = 0
            for tweet in filtered_tweets[day]:
                user_id = tweet.get_user_id()
                if user_id not in unique_users:
                    unique_users.append(user_id)
                    followers.append(tweet.user.followers_count)
            results[day] = statistics.mean(followers)
            
    if calc == 'avg_favorite_count':
        for day in filtered_tweets.keys():
            favorites = []
            for tweet in filtered_tweets[day]:
                if tweet.retweet:
                    favorites.append(tweet.retweet.get_favorite_count())
            results[day] = statistics.mean(favorites)
        
    if calc == 'retweets_and_likes_to_replies':
        for day in filtered_tweets.keys():
            ratios = []
            for tweet in filtered_tweets[day]:
                likes = 0
                retweets = 0
                replies = 0
                if tweet.retweet:
                    retweets += 1
                    likes += tweet.retweet.get_favorite_count()
                if tweet.is_reply:
                    replies += 1
                ratios.append((likes+retweets)/replies)
            results[day] = statistics.median(ratios)
    
    return results

