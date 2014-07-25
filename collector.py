""" Define the class which listens to the twitter stream and run it. """

import sys

from tweepy import Stream, OAuthHandler

import sw_auth as swa
from skatewords import StdOutListener

# authorize bot
auth = OAuthHandler(swa.consumer_key, swa.consumer_secret)
auth.set_access_token(swa.access_token, swa.access_token_secret)

try:
    # run stream
    l = StdOutListener()
    stream = Stream(auth, l)
    stream.filter(track=['skateboard','skateboarding','skateboarder'])
except KeyboardInterrupt:
    print "Stopping twitter stream collector."
    sys.exit()
