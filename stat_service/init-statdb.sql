CREATE TABLE IF NOT EXISTS likes (
    post_id UInt64,
    user_id UInt64
) ENGINE = Kafka
SETTINGS
    kafka_broker_list = 'broker:31341',
    kafka_topic_list = 'likes',
    kafka_group_name = 'likes',
    kafka_format = 'JSONEachRow';

CREATE TABLE IF NOT EXISTS views (
    post_id UInt64,
    user_id UInt64
) ENGINE = Kafka
SETTINGS
    kafka_broker_list = 'broker:31341',
    kafka_topic_list = 'views',
    kafka_group_name = 'views',
    kafka_format = 'JSONEachRow';
