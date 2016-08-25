from tweepy.streaming import StreamListener
from tweepy import Stream
from tweepy import OAuthHandler

from textblob import TextBlob

import json
import pandas as pd
import matplotlib.pyplot as plt

import myKeys

api_key = myKeys.api_key
api_secret = myKeys.api_secret
access_token_key = myKeys.access_token_key
access_token_secret = myKeys.access_token_secret

class Listener(StreamListener):

    def __init__(self):
        self.sentiment = 0
        self.last = 0

    def on_data(self, data):
        try:
            tweet = json.loads(data)
            blob = TextBlob(tweet['text'])
            # if blob.sentiment[0] == 0:
            #     return True
            # print tweet['text'], blob.sentiment[0]
            # print blob.sentiment[0]
            self.sentiment += blob.sentiment[0]
            print "{0:.2f}".format(round(blob.sentiment[0],2)), "{0:.2f}".format(round(self.getSentiment(),2)) # , "{0:.2f}".format(round(blob.sentiment[0]-self.last,2))
            # self.last = blob.sentiment[0]
        except UnboundLocalError:
            raise UnboundLocalError
        except:
            pass
        return True

    def getSentiment(self):
        return self.sentiment

    def on_error(self, status):
        print "Error: ", status

listener = Listener()
auth = OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token_key, access_token_secret)

stream = Stream(auth, listener)

# locations=-122.75,36.8, -121.75,37.8
# count = 2000
stream.filter(languages = ['en'],track = ['red', 'green','blue'], count = 2000)

listener.getSentiment()
