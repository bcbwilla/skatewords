""" Skatewords - A summary of twitter skateboarding"""

import json
import re
import string
from datetime import datetime, timedelta

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from pymongo import MongoClient

import sw_auth as swa


class StdOutListener(StreamListener):
    """ Listen to the twitter stream and put wanted tweets
        in database.
    """

    def __init__(self, db="skate_tweets",collection="tweets"):
        client = MongoClient()
        db = client[db]
        self.tweets_collection = db[collection]


    def on_data(self, data):
        tweet = json.loads(data)
        self.save_tweet(tweet)
        return True


    def on_error(self, status):
        print status


    def trim_response(self, tweet):
        """Keep only the important bits of the tweet"""

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


    def save_tweet(self, tweet):
        tweet = self.trim_response(tweet)
        tweet['time'] = datetime.now()
        self.tweets_collection.insert(tweet)



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

        self.TWEET_FILTER = "(@[A-Za-z0-9]+)|(#[A-Za-z0-9]+)|(skat[A-Za-z0-9 ]+)|(rt )|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"
        self.HASHTAG_FILTER = "(@[A-Za-z0-9]+)|(#[A-Za-z0-9]+)|(rt )|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"


    def build_text(self,text_type):

        if text_type == "tweet":
            # put tweets all in one big string
            text = ' '.join([t['text'] for t in self.data])
            re_filter = self.TWEET_FILTER
        elif text_type == "hashtag":
            nopls = ['skate','skateboard','skateboarding','skateboarder','skating'
                    'sk8boarder','skater','sk8','sk8board','sk8boarding','sk8r','sk8ing']
            # make a list of lists of hashtags from all the tweets
            k = 'hashtags'
            hashtags = [t[k] for t in self.data if t[k]]
            # compress all hashtags into a single space-separated string
            text = ' '.join([x for hts in hashtags for x in hts if x not in nopls]) # phew
            re_filter = self.HASHTAG_FILTER
        else:
            return None

        return self.filter_text(text,re_filter)


    def filter_text(self, text, re_filter):
        """Removes unwanted things (e.g. mentions, links) from text"""
        return ' '.join(re.sub(re_filter, " ", text, flags=re.I).split())
