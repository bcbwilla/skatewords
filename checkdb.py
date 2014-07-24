""" Dump some stuff to the screen so I can see what's going on in the db """

from datetime import datetime, timedelta
from pymongo import MongoClient


client = MongoClient()
db = client['skate_tweets']
tweets = db['tweets']

print " Skatewords checkdb: "
print "  Number of entries in dB: %d" % tweets.count()

td = timedelta(days=1)
recent_tweets = tweets.find({"time": {"$gt": datetime.now() - td}}).count()

print "  Number collected in past 24 hr: %d" % recent_tweets

most_recent = tweets.find().sort('time',direction=-1)[0]['time'].strftime('%Y-%m-%d at %H:%M:%S')
print "  Most recent tweet added on %s EDT." % most_recent

print " Done."
