CREATE DATABASE IF NOT EXISTS statdb;

CREATE TABLE IF NOT EXISTS statdb.kafka_likes (
    post_id UInt64,
    user_id UInt64
) ENGINE = Kafka
SETTINGS
    kafka_broker_list = 'broker:31341',
    kafka_topic_list = 'likes',
    kafka_group_name = 'likes',
    kafka_format = 'JSONEachRow';

CREATE TABLE IF NOT EXISTS statdb.kafka_views (
    post_id UInt64,
    user_id UInt64
) ENGINE = Kafka
SETTINGS
    kafka_broker_list = 'broker:31341',
    kafka_topic_list = 'views',
    kafka_group_name = 'views',
    kafka_format = 'JSONEachRow';

CREATE TABLE IF NOT EXISTS statdb.kafka_liked_users (
    user_id UInt64,
    user_who_liked UInt64
) ENGINE = Kafka
SETTINGS
    kafka_broker_list = 'broker:31341',
    kafka_topic_list = 'liked_users',
    kafka_group_name = 'liked_users',
    kafka_format = 'JSONEachRow';

CREATE TABLE IF NOT EXISTS statdb.likes (
    post_id UInt64,
    user_id UInt64
) ENGINE = MergeTree
ORDER BY (post_id);

CREATE TABLE IF NOT EXISTS statdb.views (
    post_id UInt64,
    user_id UInt64
) ENGINE = MergeTree
ORDER BY (post_id);

CREATE TABLE IF NOT EXISTS statdb.liked_users (
    user_id UInt64,
    user_who_liked UInt64
) ENGINE = MergeTree
ORDER BY (user_id);

CREATE MATERIALIZED VIEW IF NOT EXISTS statdb.kafka_mapper_likes
TO statdb.likes AS
SELECT *
FROM statdb.kafka_likes;

CREATE MATERIALIZED VIEW IF NOT EXISTS statdb.kafka_mapper_views
TO statdb.views AS
SELECT *
FROM statdb.kafka_views;

CREATE MATERIALIZED VIEW IF NOT EXISTS statdb.kafka_mapper_liked_users
TO statdb.liked_users AS
SELECT *
FROM statdb.kafka_liked_users;
