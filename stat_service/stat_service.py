import os
import time
from concurrent import futures

import grpc
import stat_service_pb2
import stat_service_pb2_grpc
import clickhouse_driver

# Stat Service

# !!!!!
# To make likes/views unique by each user, pass `DISTINCT user_id` into count() in SQL request
# !!!!!

class StatService(stat_service_pb2_grpc.StatServiceServicer):
    def __init__(self):
        host, port = os.environ.get("CLICKHOUSE_URL").split(':')
        time.sleep(10)
        self.client = clickhouse_driver.Client(host=host, port=port)
    
    def GetPostStatistics(self, request, context):
        likes = self.client.execute(f'SELECT count() FROM statdb.likes WHERE post_id = {request.post_id}')[0][0]
        views = self.client.execute(f'SELECT count(DISTINCT user_id) FROM statdb.views WHERE post_id = {request.post_id}')[0][0]
        return stat_service_pb2.PostStatisticsResponse(likes=likes, views=views)

    def GetTopPosts(self, request, context):
        cat = 'likes' if request.sort_by_likes else 'views'
        top_posts = self.client.execute(f'SELECT post_id, COUNT(*) AS {cat} FROM statdb.{cat} GROUP BY post_id ORDER BY {cat} DESC LIMIT 5')

        result = stat_service_pb2.TopPostsResponse()
        for post in top_posts:
            result.posts.append(stat_service_pb2.TopPost(post_id=post[0], score=post[1]))
        return result

    def GetTopUsers(self, request, context):
        top_users = self.client.execute('SELECT user_id, COUNT(*) AS likes FROM statdb.liked_users GROUP BY user_id ORDER BY likes DESC LIMIT 3')

        result = stat_service_pb2.TopUsersResponse()
        for user in top_users:
            result.users.append(stat_service_pb2.UserStatistics(id=user[0], likes=user[1]))
        return result

    
    

# Run
if __name__ == '__main__':
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    stat_service_pb2_grpc.add_StatServiceServicer_to_server(StatService(), server)

    server.add_insecure_port('[::]:54321')
    server.start()
    server.wait_for_termination()
