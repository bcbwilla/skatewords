skatewords
=========

Skatewords listens for skateboarding related tweets and generates daily [word cloud](http://en.wikipedia.org/wiki/Tag_cloud) summaries which are tweeted at [@skatewords](https://twitter.com/skatewords).

This is currently in an experimental stage (i.e. I have no idea what I'm doing), and new features will most likely (i.e. possibly maybe) be added in the future (i.e. not right now).

stuff for the boring
--------------------
Tweets are pulled from Twitter's [streaming API](https://dev.twitter.com/docs/api/streaming) using [Tweepy](http://www.tweepy.org/) and dumped in a [MongoDB](http://www.mongodb.org/) database.  Word clouds are generated every 24 hours using [pytagcloud](https://pypi.python.org/pypi/pytagcloud) and then [tweeted](http://www.twitter.com/skatewords).

contributing
------------
There are lots of ways you can contribute.

 - Tell others about skatewords (preferably people with predispositions to contributing to open source skateboarding related twitter bots).
 - Tweet the [author](https://www.twitter.com/bcbwilla) about any strange behvior / bugs / cool things you'd like to see added.
 - [Follow](https://twitter.com/skatewords) and send compliments.

More silly skateboarding analytics on the [author's blog](http://www.electronexchange.net).
