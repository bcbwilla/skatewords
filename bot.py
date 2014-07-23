""" Generate word clouds and post tweet image """

from datetime import datetime
import os
import logging

from tweepy import OAuthHandler, API
from pytagcloud import create_tag_image, make_tags
from pytagcloud.lang.counter import get_tag_counts

from skatewords import TextBuilder
import sw_auth as swa


LOG_FILENAME = 'the.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

# get textbuilder, which will help get text from database
tb = TextBuilder()


def make_cloud(cloud_type,time,maxsize=90,cutoff=70):
    """ Make word cloud. Returns path to image file"""

    text = tb.build_text(cloud_type)

    filename = "images/" + cloud_type + "_" + time + ".jpeg"
    tags = make_tags(get_tag_counts(text), minsize=40, maxsize=maxsize)[:cutoff]
    create_tag_image(tags, filename, background=(245,246,245),size=(900, 600), layout=2)

    return filename


# go
time = datetime.now().strftime("%Y-%m-%d--%H-%M-%S-%f")
logging.info("  " + time + " --- Making tag clouds")

hashtag_img = make_cloud("hashtag",time,maxsize=70,cutoff=50)
tweet_img = make_cloud("tweet",time)

logging.info("    Tweeting images.")

# authorize bot
auth = OAuthHandler(swa.consumer_key, swa.consumer_secret)
auth.set_access_token(swa.access_token, swa.access_token_secret)
api = API(auth)

# Send the tweet with photo
status = 'top twitter skatewords of the day'
api.update_with_media(tweet_img, status=status)

status = 'top skateboarding hashtags of the day'
api.update_with_media(hashtag_img, status=status)

logging.info("    Removing image files")
os.remove(tweet_img)
os.remove(hashtag_img)
logging.info("    Done! \n")
