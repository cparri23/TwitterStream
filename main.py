import credentials
import pandas as pd
import numpy as np
import datetime

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import Cursor
from tweepy import API

class TwitterClient():
    def __init__(self, twitterUser = None):
        self.auth = TwitterAuthenticator().authenticate()
        self.client = API(self.auth, wait_on_rate_limit=True)
        self.twitterUser = twitterUser

    def get_twitter_client_api(self):
        return self.client

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

class TweetAnalyzer():
    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame()
        timeStamps = [tweet.created_at for tweet in tweets]
        hourCreated = []
        timeZoneAdjust = datetime.timedelta(hours = 3)
        print(timeZoneAdjust)
        for ts in timeStamps:
            EST_Hour = (ts - timeZoneAdjust).hour
            hourCreated.append(EST_Hour)
            # len_timeStamp = len(ts)
            # hourTens_index = len(ts) - 8
            # hourOnes_index = len(ts) - 7
            # hourTens = ts[hourTens_index]
            # hourOnes = ts[hourOnes_index]
            # hc = (10 * hourTens) + hourOnes
            #

        df['Hour Created'] = np.array(hourCreated)
        df['text'] = np.array([tweet.text for tweet in tweets])
        return df
    pass

if __name__ == "__main__":
    client = TwitterClient()
    api = client.get_twitter_client_api()
    analyzer = TweetAnalyzer()

    myHomeTweets = client.get_home_timeline_tweets(100)

    tweetData = analyzer.tweets_to_data_frame(myHomeTweets)
    print(tweetData)

    #streamer = TwitterStreamer()
    #streamer.stream_tweets(outputFile, keyWords)