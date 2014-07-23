"""Get twitter application authorization information from super secret config file"""

import yaml

f = open('../config/config.yaml', 'r')
config = yaml.load(f)
f.close()

consumer_key = config['consumer_key']
consumer_secret = config['consumer_secret']
access_token = config['access_token']
access_token_secret = config['access_token_secret']
