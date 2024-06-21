
import unittest
from unittest.mock import MagicMock
from post_service import PostService
import grpc
import post_service_pb2
import post_service_pb2_grpc

class SloppySet:
    def __init__(self):
        self.db = dict()
        self.i = 0

    def add(self, value):
        self.db[self.i] = value
        self.i += 1

    def delete(self, key_value):
        key = None
        for id, value in self.db.items():
            if value == key_value:
                key = id
        if key:
            self.db.pop(key)

    def get(self, post_id):
        for id, value in self.db.items():
            if id == post_id:
                return value
            
        return None


class MockDB:
    def __init__(self):
        self.db = SloppySet()

    def create_engine(self, str):
        pass

    def add(self, value):
        self.db.add(value)

    def query(self, X):
        return self.db
    
    def delete(self, value):
        self.db.delete(value)

    def commit(self):
        pass

class TestPostServiceService(unittest.TestCase):
    def test_create(self):
        service = PostService(MockDB())
        response1 = service.CreatePost(post_service_pb2.CreatePostRequest(user_id=1, title='aaa', content='bbb'), None)
        response2 = service.CreatePost(post_service_pb2.CreatePostRequest(user_id=2, title='', content='aa'), None)
        response3 = service.CreatePost(post_service_pb2.CreatePostRequest(user_id=1, title='xxxxxx', content='xxxxxx'), None)
        response4 = service.CreatePost(post_service_pb2.CreatePostRequest(user_id=1, title='ashdddpasmda', content='adms;dmdm;a'), None)
    
    def test_get(self):
        service = PostService(MockDB())

        create_response = service.CreatePost(post_service_pb2.CreatePostRequest(user_id=1, title='aaa', content='bbb'), None)
        get_response = service.GetPost(post_service_pb2.GetPostRequest(id=create_response.id), None)
        self.assertEqual(get_response.title, 'aaa')
        self.assertEqual(get_response.content, 'bbb')
        self.assertEqual(get_response.user_id, 1)

    def test_get2(self):
        service = PostService(MockDB())

        create_response1 = service.CreatePost(post_service_pb2.CreatePostRequest(user_id=1, title='aaa', content='bbb'), None)
        create_response2 = service.CreatePost(post_service_pb2.CreatePostRequest(user_id=2, title='xxxx', content='yyyy'), None)
        get_response1 = service.GetPost(post_service_pb2.GetPostRequest(id=0), None)
        get_response2 = service.GetPost(post_service_pb2.GetPostRequest(id=1), None)
        self.assertEqual(get_response1.user_id, 1)
        self.assertEqual(get_response2.user_id, 2)
