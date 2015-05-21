DROP SCHEMA IF EXISTS tweet_data CASCADE;
CREATE SCHEMA tweet_data;

DROP TABLE IF EXISTS tweet_data.tweets;
CREATE TABLE tweet_data.tweets (
  id SERIAL PRIMARY KEY,
  tweet_id BIGINT,
  user_id BIGINT,
  screen_name VARCHAR(255),
  user_bio VARCHAR(255),
  text VARCHAR(200),
  user_favs INTEGER,
  friends_count INTEGER,
  created_at TIMESTAMPTZ,
  CONSTRAINT tweet UNIQUE (tweet_id, user_id)
);

