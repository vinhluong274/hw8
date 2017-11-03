# Import statements
import unittest
import sqlite3
import requests
import json
import re
import tweepy
import twitter_info # still need this in the same directory, filled out

consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Set up library to grab stuff from twitter with your authentication, and return it in a JSON format
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

umsi_tweets = api.search('umsi')

CACHE_FNAME = "twitter_cache.json"

cache_file = open(CACHE_FNAME,'r')
cache_contents = cache_file.read()
cache_file.close()
CACHE_DICTION = json.loads(cache_contents)

print(CACHE_DICTION)
