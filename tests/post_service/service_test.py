import grpc
import post_service_pb2
import unittest
import post_service_pb2_grpc

class PostServiceTest(unittest.TestCase):
    def test_posting(self):
        post_channel = grpc.insecure_channel('localhost:12345')
        grpc_post_client = post_service_pb2_grpc.PostServiceStub(post_channel)

        post = post_service_pb2.CreatePostRequest(user_id=1, title='poker', content='docker')
        response = grpc_post_client.CreatePost(post)

        post = post_service_pb2.GetPostRequest(id=response.id)
        response = grpc_post_client.GetPost(post)

        self.assertEqual(response.user_id, 1)
        self.assertEqual(response.title, 'poker')
        self.assertEqual(response.content, 'docker')

        post = post_service_pb2.UpdatePostRequest(id=response.id, user_id=1, title='aaaa', content='bbbbb')
        response = grpc_post_client.UpdatePost(post)

        post = post_service_pb2.GetPostRequest(id=response.id)
        response = grpc_post_client.GetPost(post)

        self.assertEqual(response.user_id, 1)
        self.assertEqual(response.title, 'aaaa')
        self.assertEqual(response.content, 'bbbbb')


if __name__ == '__main__':
    unittest.main()

