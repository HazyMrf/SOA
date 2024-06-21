from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from confluent_kafka import Producer
import json
import os

import grpc
import post_service_pb2
import post_service_pb2_grpc
import stat_service_pb2
import stat_service_pb2_grpc
from google.protobuf.json_format import MessageToDict
from google.protobuf.empty_pb2 import Empty

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI")
app.config['GRPC_POST_SERVICE'] = os.environ.get("GRPC_POST_SERVICE")
app.config['GRPC_STAT_SERVICE'] = os.environ.get("GRPC_STAT_SERVICE")
app.config['KAFKA_BROKER_URL'] = os.environ.get("KAFKA_BROKER_URL")
app.config['CLICKHOUSE_URL'] = os.environ.get("CLICKHOUSE_URL")
app.config['CLICKHOUSE_USER'] = os.environ.get("CLICKHOUSE_USER")
app.config['CLICKHOUSE_PASS'] = os.environ.get("CLICKHOUSE_PASS")
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)

post_channel = grpc.insecure_channel(app.config['GRPC_POST_SERVICE'])
grpc_post_client = post_service_pb2_grpc.PostServiceStub(post_channel)

stat_channel = grpc.insecure_channel(app.config['GRPC_STAT_SERVICE'])
grpc_stat_client = stat_service_pb2_grpc.StatServiceStub(stat_channel)

kafka_broker = Producer({'bootstrap.servers': app.config['KAFKA_BROKER_URL']})

def DetailedError(e: grpc.RpcError):
    return jsonify({"grpc_error": str(e.code()), "error_details": e.details()})

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(512))

    # Additional info
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    birth_date = db.Column(db.Date)
    email = db.Column(db.String(120), unique=True)
    phone_number = db.Column(db.String(20))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'User already exists'}), 409

    new_user = User(username=data['username'])
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        login_user(user)
        return jsonify({'message': 'Logged in successfully'}), 200
    return jsonify({'message': 'Invalid username or password'}), 401

@app.route('/update_profile', methods=['PUT'])
@login_required
def update_profile():
    user_data = request.get_json()
    current_user.first_name = user_data.get('first_name', current_user.first_name)
    current_user.last_name = user_data.get('last_name', current_user.last_name)
    current_user.birth_date = user_data.get('birth_date', current_user.birth_date)
    current_user.email = user_data.get('email', current_user.email)
    current_user.phone_number = user_data.get('phone_number', current_user.phone_number)
    
    db.session.commit()
    
    return jsonify({"message": "Profile updated successfully"}), 200

@app.route('/posts', methods=['POST'])
@login_required
def create_post():
    data = request.get_json()
    try:
        post = post_service_pb2.CreatePostRequest(user_id=current_user.id, title=data['title'], content=data['content'])
        response = grpc_post_client.CreatePost(post)
        return jsonify(MessageToDict(response, preserving_proto_field_name=True))
    except grpc.RpcError as e:
        return DetailedError(e), 500

@app.route('/posts/<int:id>', methods=['PUT'])
@login_required
def update_post(id):
    data = request.get_json()
    try:
        post = post_service_pb2.UpdatePostRequest(id=id, user_id=current_user.id, title=data['title'], content=data['content'])
        response = grpc_post_client.UpdatePost(post)
        return jsonify(MessageToDict(response, preserving_proto_field_name=True))
    except grpc.RpcError as e:
        return DetailedError(e), 500
    
@app.route('/posts/<int:id>', methods=['DELETE'])
@login_required
def delete_post(id):
    try:
        post = post_service_pb2.DeletePostRequest(id=id, user_id=current_user.id)
        response = grpc_post_client.DeletePost(post)
        return jsonify(MessageToDict(response, preserving_proto_field_name=True))
    except grpc.RpcError as e:
        return DetailedError(e), 500

@app.route('/posts/<int:id>', methods=['GET'])
@login_required
def get_post(id):
    try:
        post = post_service_pb2.GetPostRequest(id=id)
        response = grpc_post_client.GetPost(post)
        return jsonify(MessageToDict(response, preserving_proto_field_name=True))
    except grpc.RpcError as e:
        return DetailedError(e), 500
    
@app.route('/posts', methods=['GET'])
@login_required
def list_posts():
    data = request.get_json()
    try:
        post = post_service_pb2.ListPostsRequest(page_number=int(data['page_number']), posts_per_page=int(data['posts_per_page']))
        response = grpc_post_client.ListPosts(post)
        return jsonify(MessageToDict(response, preserving_proto_field_name=True))
    except grpc.RpcError as e:
        return DetailedError(e), 500
    
def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

@app.route('/posts/<int:post_id>/view', methods=['POST'])
def post_view(post_id):
    data = {'post_id': post_id, 'user_id': current_user.id}
    kafka_broker.produce('views', key=str(post_id), value=json.dumps(data), callback=delivery_report)
    kafka_broker.flush()
    return jsonify({f'Post {post_id} viewed by' : current_user.id}), 200

@app.route('/posts/<int:post_id>/like', methods=['POST'])
def post_like(post_id):
    data = {'post_id': post_id, 'user_id': current_user.id}
    kafka_broker.produce('likes', key=str(post_id), value=json.dumps(data), callback=delivery_report)
    kafka_broker.flush()

    post = post_service_pb2.GetPostRequest(id=post_id)
    response = grpc_post_client.GetPost(post)
    data_liked = {'user_id': response.user_id, 'user_who_liked': current_user.id}
    kafka_broker.produce('liked_users', key=str(post_id), value=json.dumps(data_liked), callback=delivery_report)

    return jsonify({f'Post {post_id} liked by' : current_user.id}), 200

@app.route('/posts/<int:post_id>/statistics', methods=['GET'])
@login_required
def get_post_statistics(post_id):
    try:
        post = stat_service_pb2.PostStatisticsRequest(post_id=post_id)
        response = grpc_stat_client.GetPostStatistics(post)
        return jsonify(MessageToDict(response, preserving_proto_field_name=True))
    except grpc.RpcError as e:
        return DetailedError(e), 500

@app.route('/posts/top_liked', methods=['GET'])
@login_required
def get_top_liked():
    try:
        result = []
        post = stat_service_pb2.TopPostsRequest(sort_by_likes=True)
        response = grpc_stat_client.GetTopPosts(post)
        for post in response.posts:
            post_req = post_service_pb2.GetPostRequest(id=post.post_id)
            post_info = grpc_post_client.GetPost(post_req)
            result.append({
                'post_id': post.post_id,
                'author': post_info.user_id,
                'likes': post.score
            })
        return jsonify(result)
    except grpc.RpcError as e:
        return DetailedError(e), 500
    

@app.route('/posts/top_viewed', methods=['GET'])
@login_required
def get_top_viewed():
    try:
        result = []
        post = stat_service_pb2.TopPostsRequest(sort_by_likes=False)
        response = grpc_stat_client.GetTopPosts(post)
        for post in response.posts:
            post_req = post_service_pb2.GetPostRequest(id=post.post_id)
            post_info = grpc_post_client.GetPost(post_req)
            result.append({
                'post_id': post.post_id,
                'author': post_info.user_id,
                'viewes': post.score
            })
        return jsonify(result)
    except grpc.RpcError as e:
        return DetailedError(e), 500
    
@app.route('/posts/top_users', methods=['GET'])
@login_required
def get_top_users():
    try:
        response = grpc_stat_client.GetTopUsers(Empty())
        return jsonify(MessageToDict(response, preserving_proto_field_name=True))
    except grpc.RpcError as e:
        return DetailedError(e), 500


# Run
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
