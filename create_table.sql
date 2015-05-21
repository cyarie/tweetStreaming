DROP SCHEMA IF EXISTS tweet_data CASCADE;
CREATE SCHEMA tweet_data;

DROP TABLE IF EXISTS tweet_data.tweets;
CREATE TABLE tweet_data.tweets (
  id SERIAL PRIMARY KEY,
  tweet_id INTEGER,
  user_id INTEGER,
  screen_name VARCHAR(140),
  user_bio VARCHAR(160),
  text VARCHAR(160),
  user_favs INTEGER,
  friends_count INTEGER,
  created_at TIMESTAMPTZ,
  CONSTRAINT tweet UNIQUE (tweet_id, user_id)
);

