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
        # Using logging to write tweets to a file
        self.tweet_logger = logging.getLogger("candidate_mentions")
        self.tweet_logger.setLevel(logging.INFO)
        self.handler = TimedRotatingFileHandler(os.path.join(os.getcwd(), "tweet_logs/candidate_mentions.txt"),
                                                when="d",
                                                interval=1,
                                                backupCount=30)
        self.handler.setLevel(logging.INFO)
        self.formatter = logging.Formatter("%(message)s")
        self.handler.setFormatter(self.formatter)
        self.tweet_logger.addHandler(self.handler)

        # Setting up a separate logger to handle errors
        self.error_logger = logging.getLogger("streamer_errors")
        self.error_logger.setLevel(logging.ERROR)
        self.handler = TimedRotatingFileHandler("streamer_errors.txt",
                                                when="d",
                                                interval=1,
                                                backupCount=30)
        self.handler.setLevel(logging.ERROR)
        self.formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
        self.handler.setFormatter(self.formatter)
        self.error_logger.addHandler(self.handler)

    def on_data(self, raw_data):
        try:
            decoded = json.loads(raw_data)
            if decoded["user"]["description"] is not None:
                user_bio = decoded["user"]["description"].encode("ascii", "replace")
            else:
                user_bio = "None"
            tweet_dict = {
                "id": decoded["id"],
                "created_at": decoded["created_at"],
                "text": decoded["text"].encode("ascii", "replace"),
                "friends_count": decoded["user"]["friends_count"],
                "user_favs": decoded["user"]["favourites_count"],
                "screen_name": decoded["user"]["screen_name"],
                "user_id": decoded["user"]["id"],
                "user_bio": user_bio,
            }
            self.tweet_logger.info(tweet_dict)
            return True
        except Exception as e:
            self.error_logger.error(e)

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