import credentials

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

class StdOutListener(StreamListener):
        def on_data(self, data):
            print(data)
            return True

        def on_error(self, status):
            print(status)
            return

if __name__ == "__main__":
    listener = StdOutListener()
    auth = OAuthHandler(credentials.API_KEY, credentials.API_SECRET_KEY)
    auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)

    stream = Stream(auth, listener)

    stream.filter(track=['rat'])