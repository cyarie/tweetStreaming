import os
import logging

from boto.s3.connection import S3Connection
from boto.s3.key import Key
from datetime import date, timedelta

# Setup logging for monitoring when these tweets go to S3.
logger = logging.getLogger("upload_tweets")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler = logging.FileHandler("tweets_uploader.log")
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)

logger.addHandler(handler)


def upload_files():
    tweet_dir = os.path.join(os.getcwd(), "tweet_logs")
    base_file_name = "candidate_mentions.txt.{0}"
    conn = S3Connection(os.getenv("AWS_ACCESS_KEY_ID"), os.getenv("AWS_SECRET_ACCESS_KEY"))
    tweet_bucket = conn.get_bucket("cyarie-tweet-data")
    for x in range(1, 8):
        file_date = (date.today() - timedelta(days=x)).strftime("%Y-%m-%d")
        k = Key(tweet_bucket)
        key_name = base_file_name.format(file_date)
        k.key = key_name
        try:
            file_name = os.path.join(tweet_dir, base_file_name.format(file_date))
            k.set_contents_from_filename(file_name)
            logger.info("{0} uploaded to S3".format(file_name))
        except FileNotFoundError as e:
            logger.error("Error uploading file to S3: {0}".format(e))


def main():
    upload_files()

if __name__ == "__main__":
    main()