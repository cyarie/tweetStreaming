import psycopg2
import csv
import os


def db_connect():
    try:
        conn = psycopg2.connect("dbname='{0}' "
                                "user='{0}' "
                                "host='{1}' "
                                "password='{2}' "
                                "port=5432 ".format(os.getenv("PITCHES_DB_NAME"),
                                                    os.getenv("PITCHES_DB_HOST"),
                                                    os.getenv("PITCHES_DB_PW"),))
        return conn
    except psycopg2.OperationalError as e:
        print("Error connection to the database: ", e)


def build_db():
    tweets_loc = "/home/tweets-deploy/tweetStreaming/tweets_csvs/tweets_master_csv.csv"
    tweet_sql = """
    INSERT INTO tweet_data.tweets (tweet_id, user_id, screen_name, user_bio, text, user_favs, friends_count, created_at)
    VALUES (%(tweet_id)s, %(user_id)s, %(screen_name)s, %(user_bio)s, %(text)s, %(user_favs)s, %(friends_count)s,
            %(created_at)s)
    """
    with open(tweets_loc, "r", newline="") as tweets:
        db_conn = db_connect()
        cursor = db_conn.cursor()
        csv_reader = csv.DictReader(tweets)
        print("STARTING THE TWEETS!")
        for tweet in csv_reader:
            cursor.execute(tweet_sql, tweet)
            db_conn.commit()
        db_conn.close()
    print("FINISHED WITH THE TWEETS!")


def main():
    build_db()


if __name__ == "__main__":
    main()
