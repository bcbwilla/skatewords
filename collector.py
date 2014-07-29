""" Define the class which listens to the twitter stream and run it. """

import sys

from tweepy import Stream, OAuthHandler

import sw_auth as swa
from skatewords import StdOutListener

# authorize bot
auth = OAuthHandler(swa.consumer_key, swa.consumer_secret)
auth.set_access_token(swa.access_token, swa.access_token_secret)

# what to listen for
track_list = ['skateboard','skateboarding','skateboarder','skateboards',
    'skateboarders','sk8board','sk8boarding','sk8boarders','sk8boards']

try:
    # run stream
    l = StdOutListener()
    stream = Stream(auth, l)
    stream.filter(track=track_list)
except KeyboardInterrupt:
    print "\nStopping twitter stream collector."
    sys.exit()
