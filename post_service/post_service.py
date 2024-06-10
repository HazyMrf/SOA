import os
from concurrent import futures
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, scoped_session

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey

import grpc
import post_service_pb2
import post_service_pb2_grpc

# Wrappers

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db.create_engine(os.environ.get("DATABASE_URI")))

Base = declarative_base()
class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    user_id = Column(Integer)

def PostToPB(post: Post):
    return post_service_pb2.Post(id=post.id, title=post.title, content=post.content, user_id=post.user_id)

# Post Service

class PostService(post_service_pb2_grpc.PostServiceServicer):
    def __init__(self):
        self.session = SessionLocal()

    def CreatePost(self, request, context):
        post = Post(title=request.title, content=request.content, user_id=request.user_id)
        self.session.add(post)
        self.session.commit()
        return PostToPB(post)
    
    def UpdatePost(self, request, context):
        post = self.session.query(Post).filter(Post.id == request.id).first()
        if post and post.user_id == request.user_id:
            post.title = request.title
            post.content = request.content
            self.session.commit()
            return PostToPB(post)
        elif not post:
            context.abort(grpc.StatusCode.NOT_FOUND, 'Post not found')
        else:
            context.abort(grpc.StatusCode.PERMISSION_DENIED, 'Permission denied')
    
    def DeletePost(self, request, context):
        post = self.session.query(Post).filter(Post.id == request.id).first()
        if post and post.user_id == request.user_id:
            self.session.delete(post)
            self.session.commit()
            return PostToPB(post)
        elif not post:
            context.abort(grpc.StatusCode.NOT_FOUND, 'Post not found')
        else:
            context.abort(grpc.StatusCode.PERMISSION_DENIED, 'Permission denied')
    
    def GetPost(self, request, context):
        post = self.session.query(Post).get(request.id)
        if post:
            return PostToPB(post)
        else:
            context.abort(grpc.StatusCode.NOT_FOUND, 'Post not found')

    def ListPosts(self, request, context):
        query = self.session.query(Post)
        posts_count = query.count()
        posts = query.offset((request.page_number - 1) * request.posts_per_page).limit(request.posts_per_page).all()
        return post_service_pb2.ListPostsResponse(posts=[PostToPB(post) for post in posts], posts_count=posts_count)

# Run
if __name__ == '__main__':
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    post_service_pb2_grpc.add_PostServiceServicer_to_server(PostService(), server)

    server.add_insecure_port('[::]:12345')
    server.start()
    server.wait_for_termination()
