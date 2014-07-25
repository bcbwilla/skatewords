""" Skatewords - A summary of twitter skateboarding"""

import json
import re
import string
from datetime import datetime, timedelta

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from pymongo import MongoClient
from nltk.corpus import stopwords

import sw_auth as swa


class StdOutListener(StreamListener):
    """ Listen to the twitter stream and put wanted tweets
        in database.
    """

    def __init__(self, db="skate_tweets",collection="tweets"):
        """ Set up database """
        client = MongoClient()
        db = client[db]
        self.tweets_collection = db[collection]


    def on_data(self, data):
        """ Convert, trim and store tweet info in database """
        tweet = json.loads(data)
        tweet = self.trim_response(tweet)
        tweet['time'] = datetime.now()
        self.tweets_collection.insert(tweet)
        return True


    def on_error(self, status):
        print status


    def trim_response(self, tweet):
        """ Keep only the important bits of the tweet """

        trimmed = {}
        trimmed['text'] = tweet['text']
        trimmed['hashtags'] = [v['text'].lower() for v in tweet['entities']['hashtags']]
        trimmed['followers'] = tweet['user']['followers_count']

        user_mentions = tweet['entities']['user_mentions']
        if user_mentions:
            user_mentions = [um['screen_name'] for um in user_mentions]

        trimmed['user_mentions'] = user_mentions

        coordinates = tweet['coordinates']
        if coordinates:
            coordinates = tweet['coordinates']['coordinates'][::-1]

        trimmed['coordinates'] = coordinates

        return trimmed


class TextBuilder(object):
    """ Generate word clouds """


    def __init__(self,cutoff_age='',db='skate_tweets',collection='tweets'):
        client = MongoClient()
        db = client[db]
        self.tweets_collection = db[collection]

        if cutoff_age and type(cutoff_age) is int:
            td = timedelta(days=cutoff_age)
            self.data = list(self.tweets_collection.find({"time": {"$gt": datetime.now() - td}}))
        else:
            self.data = list(self.tweets_collection.find())

        self.re_filter = "(@[A-Za-z0-9]+)|(#[A-Za-z0-9]+)|(rt )|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"

        # get list of words to filter. use custom list and all stopwords from nltk
        self.stopwords = [line.strip() for line in open('stopwords.txt', 'r')] + stopwords.words()


    def build_text(self,text_type):
        """ Returns a single text string (or None).
            text_type -- tweet or hashtag
        """

        texts = []
        if text_type == 'tweet':
            # put tweets all in one big string
            for tweet in self.data:
                texts.append(tweet['text'].lower())
        elif text_type == 'hashtag':
            for tweet in self.data:
                texts.append(' '.join(ht.lower() for ht in tweet['hashtags']))
        else:
            return None

        final_text = '' # what the word cloud will be made of
        for text in texts:
            # initial regex processing to remove puntuation, urls, mentionsm etc.
            text = ' '.join(re.sub(self.re_filter, " ", text, flags=re.I).split())
            text = ' '.join([word for word in text.split() if self.keep_word(word)]) # word
            
            final_text += text

        return final_text


    def keep_word(self, word):
        """ Returns false if word is in stopwords or non ascii """
        
        # keep only ascii words
        try:
            word.encode('ascii')
        except (UnicodeEncodeError, UnicodeDecodeError):
            return False
        else:
            
            # remove stop words
            if word not in self.stopwords:
                return True
            else:
                return False
