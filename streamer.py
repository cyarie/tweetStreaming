import os
import json
import sys

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream


access_token = os.getenv("T_ACCESS_TOKEN")
access_token_secret = os.getenv("T_ACCESS_TOKEN_SECRET")
consumer_key = os.getenv("T_CONSUMER_KEY")
consumer_secret = os.getenv("T_CONSUMER_SECRET")


# Setup a listener class to plug into the Twitter Streaming API
class TweetListener(StreamListener):

    def on_data(self, raw_data):
        try:
            decoded = json.loads(raw_data)
            tweet_dict = {
                "id": decoded["id"],
                "text": decoded["text"].encode("ascii", "ignore"),
                "retweeted": decoded["retweeted"],
                "retweet_count": decoded["retweet_count"],
                "followers_count": decoded["user"]["followers_count"],
                "friends_count": decoded["user"]["friends_count"],
            }
            sys.stdout.write(tweet_dict)
            return True
        except Exception as e:
            print(e)

    def on_error(self, status_code):
        print(status_code)


def main():
    listener = TweetListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, listener)

    try:
        stream.filter(track=['scott walker', 'marco rubio', 'rand paul', 'ted cruz', 'jeb bush'], languages=['en'])
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()