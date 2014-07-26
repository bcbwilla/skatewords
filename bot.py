""" Generate word clouds and post tweet image """

from datetime import datetime
import os
import logging
import sys

from tweepy import OAuthHandler, API
from pytagcloud import create_tag_image, make_tags
from pytagcloud.lang.counter import get_tag_counts

from skatewords import TextBuilder
import sw_auth as swa


LOG_FILENAME = 'the.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

# get textbuilder, which will help get text from database
tb = TextBuilder(cutoff_age=1)
num_tweets = tb.tweets_collection.count()


def make_cloud(cloud_type,time,maxsize=80,cutoff=65,layout=4):
    """ Make word cloud. Returns path to image file"""

    text = tb.build_text(cloud_type)

    filename = "images/" + cloud_type + "_" + time + ".png"
    tags = make_tags(get_tag_counts(text), minsize=30, maxsize=maxsize)

    if len(tags) >= cutoff:
    	tags = tags[:cutoff]
    else:
    	return None

    if tags:
        create_tag_image(tags, filename, background=(0,0,0),size=(900, 600), layout=layout)
        return filename
    else:
    	return None


# go
time = datetime.now().strftime("%Y-%m-%d--%H-%M-%S-%f")
logging.info("  " + time + " --- Making tag clouds")

hashtag_img = make_cloud("hashtag",time,maxsize=60,cutoff=50,layout=2)
tweet_img = make_cloud("tweet",time)


if len(sys.argv) == 2 and sys.argv[1] == 'test':
    logging.info("    This is a test, not tweeting images.")
else:
    logging.info("    Tweeting images.")

    # authorize bot
    auth = OAuthHandler(swa.consumer_key, swa.consumer_secret)
    auth.set_access_token(swa.access_token, swa.access_token_secret)
    api = API(auth)

    # send the tweet with photo
    if tweet_img:
        status = 'top skatewords of the day from %d tweets' % num_tweets
        api.update_with_media(tweet_img, status=status)
        os.remove(tweet_img)

    if hashtag_img:
        status = 'top skateboarding hashtags of the day from %d tweets' % num_tweets
        api.update_with_media(hashtag_img, status=status)
        os.remove(hashtag_img)

logging.info("    Done! \n")
