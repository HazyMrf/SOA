import grpc
import stat_service_pb2
import stat_service_pb2_grpc
import clickhouse_driver
import unittest


def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

class StatServiceTest(unittest.TestCase):
    def test_stat_service(self):
        client = clickhouse_driver.Client(host='statdb', port=9000)
        stat_channel = grpc.insecure_channel('localhost:54321')
        grpc_stat_client = stat_service_pb2_grpc.StatServiceStub(stat_channel)

        client.execute("INSERT INTO statdb.likes (post_id, user_id) VALUES (%s, %s), (%s, %s), (%s, %s)", (1, 4, 2, 5, 3, 6))
        client.execute("INSERT INTO statdb.views (post_id, user_id) VALUES (%s, %s), (%s, %s), (%s, %s)", (1, 4, 2, 3, 3, 4))

        post = stat_service_pb2.PostStatisticsRequest(post_id=1)
        response = grpc_stat_client.GetPostStatistics(post)

        self.assertEqual(response.likes, 1)
        self.assertEqual(response.views, 1)

if __name__ == '__main__':
    unittest.main()