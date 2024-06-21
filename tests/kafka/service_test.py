import unittest
import clickhouse_driver
from confluent_kafka import Producer
import time

def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

class KafkaTest(unittest.TestCase):
    def test_interconnection(self):
        client = clickhouse_driver.Client(host='statdb', port=9000)
        kafka_broker = Producer({'bootstrap.servers': 'broker:31341'})

        kafka_broker.produce("likes", '{"post_id":"1", "user_id":"4"}', callback=delivery_report)
        kafka_broker.produce("likes", '{"post_id":"2", "user_id":"2"}', callback=delivery_report)
        kafka_broker.produce("likes", '{"post_id":"3", "user_id":"3"}', callback=delivery_report)
        kafka_broker.produce("likes", '{"post_id":"1", "user_id":"10"}', callback=delivery_report)
        kafka_broker.produce("likes", '{"post_id":"4", "user_id":"20"}', callback=delivery_report)
        kafka_broker.flush()

        # connection flush
        client.execute("SELECT post_id, user_id FROM statdb.likes")
        time.sleep(10)

        self.assertEqual(set(client.execute("SELECT * FROM statdb.likes")), set([(1, 4), (2, 2), (3, 3), (1, 10), (4, 20)]))

if __name__ == '__main__':
    unittest.main()