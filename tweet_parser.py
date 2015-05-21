import csv
import os
import ast


def json_to_csv():
    with open("/home/tweets-deploy/tweetStreaming/tweet_logs/master_tweets.txt", "r", newline="") as tweet_file:
        csv_path = os.path.join(os.getcwd(), "tweets_csvs")
        tweet_csv = os.path.join(csv_path, "tweets_master_csv.csv")
        with open(tweet_csv, "w") as tweets_csv:
            headers = ["tweet_id", "user_id", "screen_name", "user_bio", "text",
                       "user_favs", "friends_count", "created_at"]
            writer = csv.DictWriter(tweets_csv, fieldnames=headers, quoting=csv.QUOTE_MINIMAL)

            writer.writeheader()
            for line in tweet_file:
                tweet_dict = ast.literal_eval(line.rstrip("\n"))

                if tweet_dict["user_bio"] != "None":
                    tweet_dict["user_bio"] = tweet_dict["user_bio"].decode("utf-8")
                if tweet_dict["text"] != "None":
                    tweet_dict["text"] = tweet_dict["text"].decode("utf-8")

                writer.writerow({"tweet_id": tweet_dict["id"],
                                 "user_id": tweet_dict["user_id"],
                                 "screen_name": tweet_dict["screen_name"],
                                 "user_bio": tweet_dict["user_bio"],
                                 "text": tweet_dict["text"],
                                 "user_favs": tweet_dict["user_favs"],
                                 "friends_count": tweet_dict["friends_count"],
                                 "created_at": tweet_dict["created_at"]})


def main():
    json_to_csv()

if __name__ == "__main__":
    main()
