import unittest
from unittest.mock import MagicMock
from stat_service import StatService
import grpc
import stat_service_pb2
import stat_service_pb2_grpc

class MockDB:
    def __init__(self):
        self.db = dict()

    def execute(self, key):
        return self.db[key]
    
    def add(self, key, value):
        self.db[key] = value


class TestStatServiceService(unittest.TestCase):
    def test_statistics(self):
        db = MockDB()
        db.add('SELECT count() FROM statdb.likes WHERE post_id = 1', [[2]])
        db.add('SELECT count() FROM statdb.views WHERE post_id = 1', [[100]])

        service = StatService(db)
        resp = service.GetPostStatistics(stat_service_pb2.PostStatisticsRequest(post_id=1), None)
        self.assertEqual(resp.likes, 2)
        self.assertEqual(resp.views, 100)


    def test_top_posts(self):
        db = MockDB()
        db.add('SELECT post_id, COUNT(*) AS likes FROM statdb.likes GROUP BY post_id ORDER BY likes DESC LIMIT 5', [[1, 100], [7, 55], [2, 34]])

        service = StatService(db)
        resp = service.GetTopPosts(stat_service_pb2.TopPostsRequest(sort_by_likes=True), None)
        self.assertEqual(resp.posts[0].post_id, 1)
        self.assertEqual(resp.posts[0].score, 100)
        self.assertEqual(resp.posts[1].post_id, 7)
        self.assertEqual(resp.posts[1].score, 55)
        self.assertEqual(resp.posts[2].post_id, 2)
        self.assertEqual(resp.posts[2].score, 34)

