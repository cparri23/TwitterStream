import credentials
import pandas as pd
import numpy as np

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import Cursor
from tweepy import API

class TwitterClient():
    def __init__(self, twitterUser = None):
        self.auth = TwitterAuthenticator().authenticate()
        self.client = API(self.auth)
        self.twitterUser = twitterUser

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.client.user_timeline, id=self.twitterUser).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_home_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.client.home_timeline, id=self.twitterUser).items(num_tweets):
            tweets.append(tweet)
        return tweets

class TwitterAuthenticator():
    def authenticate(self):
        auth = OAuthHandler(credentials.API_KEY, credentials.API_SECRET_KEY)
        auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)
        return auth
class TwitterStreamer():
    # Class for streaming tweets
    def __init__(self):
        self.TwitterAuthenticator = TwitterAuthenticator()
    def stream_tweets(self, fetchedTweetsOutputFile, keywords):
        listener = TwitterListener(fetchedTweetsOutputFile)
        auth = self.TwitterAuthenticator.authenticate()
        stream = Stream(auth, listener)
        stream.filter(track=keywords)

class TwitterListener(StreamListener):
        def __init__(self, fetchedTweetsOutputFile):
            self.fetchedTweetsOutputFile = fetchedTweetsOutputFile
        def on_data(self, data):
            try:
                print(data)
                with open(self.fetchedTweetsOutputFile, 'a') as tf:
                    tf.write(data)
            except BaseException as e:
                print("Error on data: %s" % str(e))
            return True

        def on_error(self, status):
            if(status == 420):
                return False
            print(status)
            return False

if __name__ == "__main__":
    keyWords = [" anime "]
    outputFile = "tweets.json"

    client = TwitterClient('pycon')
    print(client.get_home_timeline_tweets(5))


    #streamer = TwitterStreamer()
    #streamer.stream_tweets(outputFile, keyWords)