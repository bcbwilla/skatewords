""" Define the class which listens to the twitter stream and run it. """

from tweepy import Stream, OAuthHandler

import sw_auth as swa
from skatewords import StdOutListener

# authorize bot
auth = OAuthHandler(swa.consumer_key, swa.consumer_secret)
auth.set_access_token(swa.access_token, swa.access_token_secret)

# run stream
l = StdOutListener()
stream = Stream(auth, l)
stream.filter(track=['skateboard','skateboarding','skateboarder'])
