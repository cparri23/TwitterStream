import credentials

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import cursor
from tweepy import API

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
            print(status)
            return

if __name__ == "__main__":
    keyWords = [" anime "]
    outputFile = "tweets.json"

    streamer = TwitterStreamer()
    streamer.stream_tweets(outputFile, keyWords)