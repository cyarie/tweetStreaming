import os
import json
import logging

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from logging.handlers import TimedRotatingFileHandler


access_token = os.getenv("T_ACCESS_TOKEN")
access_token_secret = os.getenv("T_ACCESS_TOKEN_SECRET")
consumer_key = os.getenv("T_CONSUMER_KEY")
consumer_secret = os.getenv("T_CONSUMER_SECRET")


# Setup a listener class to plug into the Twitter Streaming API
class TweetListener(StreamListener):
    def __init__(self):
        super(TweetListener, self).__init__()
        self.logger = None
        self.logger = logging.getLogger("candidate_mentions")
        self.logger.setLevel(logging.INFO)
        self.handler = TimedRotatingFileHandler("candidate_mentions.txt", when="d", interval=1, backupCount=30)
        self.handler.setLevel(logging.INFO)
        self.formatter = logging.Formatter("%(message)s")
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)

    def on_data(self, raw_data):
        try:
            decoded = json.loads(raw_data)
            tweet_dict = {
                "id": decoded["id"],
                "created_at": decoded["created_at"],
                "text": decoded["text"].encode("ascii", "ignore"),
                "friends_count": decoded["user"]["friends_count"],
                "user_favs": decoded["user"]["favourites_count"],
            }
            self.logger.info(tweet_dict)
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
        stream.filter(track=['scott walker', 'marco rubio', 'rand paul', 'ted cruz', 'jeb bush', 'hillary clinton'],
                      languages=['en'])
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()