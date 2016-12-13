#!/usr/bin/env python

import tweepy, time, os, sys, yaml

# Load twitter credentials for this bot from config file
BOTCRED_FILE = '%s/.twurlrc' % os.path.expanduser('~') 
with open(BOTCRED_FILE, 'r') as credfile:
	full_config = yaml.load(credfile)
	api_key = api_key = full_config['profiles']['tpeaksdiary'].keys()[0]
	bot_creds = full_config['profiles']['tpeaksdiary'][api_key]

CONSUMER_KEY = bot_creds['consumer_key']
CONSUMER_SECRET = bot_creds['consumer_secret']
ACCESS_KEY = bot_creds['token']
ACCESS_SECRET = bot_creds['secret']

# Do actual authentication
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

BOTDIR = sys.path[0]

# Prod
TWEET_FILE    = '%s/tweet-these-scenes.txt' % BOTDIR
TWEET_ARCHIVE = '%s/tweet-archive.txt' % BOTDIR
GIF_DIR       = '%s/media' % BOTDIR

# Read gif from file
with open(TWEET_FILE, 'r') as fin:
    data = fin.read().splitlines(True)
    tweet_gif = data[0]

# Delete gif from queue tweet file
with open(TWEET_FILE, 'w') as fout:
    fout.writelines(data[1:])

# Archive gif record
with open(TWEET_ARCHIVE, 'a') as fout:
    fout.writelines(tweet_gif)

gif = '%s/%s' % (GIF_DIR, tweet_gif)
gif = gif.replace('\n', '')
api.update_with_media(gif)

# Post to Tumblr Too
# Load tumblr credentials for this bot from config file
BOTCRED_FILE = '%s/.twurlrc' % os.path.expanduser('~') 
with open(BOTCRED_FILE, 'r') as credfile:
	full_config = yaml.load(credfile)
	api_key = api_key = full_config['profiles']['twinpeaksdiarytumblr'].keys()[0]
	bot_creds = full_config['profiles']['twinpeaksdiarytumblr'][api_key]

from tumblpy import Tumblpy
TUMBLR_CONSUMER_KEY = bot_creds['consumer_key']
TUMBLR_CONSUMER_SECRET = bot_creds['consumer_secret']
OAUTH_TOKEN = bot_creds['token']
OAUTH_TOKEN_SECRET = bot_creds['secret']

t = Tumblpy(TUMBLR_CONSUMER_KEY, TUMBLR_CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
blog_url = t.post('user/info')
blog_url = blog_url['user']['blogs'][0]['url']
photo = open(gif, 'rb')
post = t.post('post', blog_url=blog_url, params={'type':'photo', 'data': photo})











