#!/usr/bin/evn python3
# -*- coding: utf-8 -*-
"""
Created on 4/29/20

@author waldo

Objects used to store a reduced set of information about a tweet. The tweet object is the basic for this group,
storing the tweet id, text, and hashtags. If the tweet is a quote or a retweet, a tweet object of the tweet
that is quoted or retweeted is also stored. A user object is also stored, showing who tweeted this.
"""
import random

class tweet(object):
    """
    A basic tweet object. Holds the tweet_id, text, any hashtags, mentions,
    a user object, and different information for retweets, quotes, and replies.
    """
    def __init__(self, js_tweet):
        if 'id_str' in js_tweet:
            self.tweet_id = js_tweet['id_str']
        else:
            self.tweet_id = 'unknown' + str(random.randint(1,1000000))
        if 'truncated' in js_tweet and js_tweet['truncated']:
            self.text = js_tweet['extended_tweet']['full_text']
        elif 'text' in js_tweet:
            self.text = js_tweet['text']
        else:
            self.text = ''
        if 'entities' in js_tweet:
            self.hashtags = []
            for h in js_tweet['entities']['hashtags']:
                self.hashtags.append(h['text'])
            self.mentions = js_tweet['entities']['user_mentions']
        if 'user' in js_tweet:
            self.user = tweet_user(js_tweet['user'])
        else:
            self.user = None
        
        if 'retweeted_status' in js_tweet:
            self.retweet = tweet(js_tweet['retweeted_status'])
            self.retweet_count = js_tweet['retweet_count']
        else:
            self.retweet = ''
        if 'in_reply_to_status_id_str' in js_tweet and js_tweet['in_reply_to_status_id_str'] != None :
            self.in_reply = t_reply(js_tweet)
        else:
            self.in_reply = ''
        if 'is_quoted_status' in js_tweet and \
                js_tweet['is_quote_status'] :
            self.quote = tweet(js_tweet['quoted_status'])
        else:
            self.quote = None
        if 'is_quote_status' in js_tweet:
            self.quote_status = js_tweet['is_quote_status']
        else:
            self.quote_status = None
        if 'favorited' in js_tweet:
            self.favorited = js_tweet['favorited']
        else:
            self.favorited = None
        if 'favorite_count' in js_tweet:
            self.favorite_count = js_tweet['favorite_count']
        else:
            self.favorite_count = 0
            
    def get_user_id(self):
        """
        Convenience function: return the id of the user who is associated with this tweet
        :return: The user_id, as a string, for the user associated with this tweet
        """
        if self.user != None:
            return self.user.user_id
        else:
            return None

    def get_user_name(self):
        """
        Convenience function: return the screen name of the user associated with this tweet
        :return: A string with the screen name of the person associated with this tweet
        """
        if self.user is None:
            return None
        else:
            return self.user.screen_name
        
    def be_retweet(self):
        """
        Convenience function: return whether or not this tweet is a retweet
        :return: True if the tweet is a retweet; False otherwise
        """
        if self.retweet != '':
            return True
        else:
            return False

    def get_retweet(self):
        """
        Convenience function: if the tweet in question is a retweet, returns the retweeted tweet
        :return: the tweet that was retweeted; None if the tweet is not a retweet
        """
        if self.retweet is '':
            return None
        else:
            return self.retweet

    def is_reply(self):
        """
        Convenience function: returns whether or not this tweet is in reply to another tweet
        :return: True if this tweet is in reply to another tweet; False otherwise
        """
        if self.in_reply == '':
            return False
        else:
            return True

    def get_reply(self):
        """
        Convenience function: if this tweet is in reply to another tweet, return the tweet to which it is a reply
        :return: The tweet this tweet is in reply to; None if this tweet is not a reply
        """
        if self.is_reply():
            return self.in_reply
        else:
            return None

    def get_favorited(self):
        if self.favorited is True:
            return True
        else:
            return False

    def get_favorite_count(self):
        return self.favorite_count

class tweet_user(object):
    """
    A user object. Holds information about the user who issued a tweet, including
    the screen name, user_id, location, description, followers and friends count,
    and if the account is verified.
    """
    def __init__(self, js_user):
        self.screen_name = js_user['name']
        self.user_id = js_user['id_str']
        self.followers_count = js_user['followers_count']
        self.friends_count = js_user['friends_count']
        self.verified = js_user['verified']
        self.total_tweets = js_user['statuses_count']
        self.account_created = js_user['created_at']

class t_reply(object):
    """
    A tweet reply object, holding information relevant only to a reply, including
    the id, author id, and author screen name of the tweet being replied to.
    """
    def __init__(self, js_tweet):
        self.original_id = js_tweet['in_reply_to_status_id_str']
        self.author_id = js_tweet['in_reply_to_user_id_str']
        self.author_screen_name = js_tweet['in_reply_to_screen_name']




