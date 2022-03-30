import os
from flask import Flask, jsonify, request

import boto3

app = Flask(__name__)

USERS_TABLE = os.environ['USERS_TABLE']
IS_OFFLINE = os.environ.get('IS_OFFLINE')
 
if IS_OFFLINE:
    client = boto3.client(
        'dynamodb',
        region_name='localhost',
        endpoint_url='http://localhost:8000'
    )
else:
    client = boto3.client('dynamodb')
# clinet = boto3.client('dynamodb')

@app.route('/')
def hello_from_root():
    return jsonify(message="Hello world")

@app.route("/hello")
def hello():
    return jsonify(message='Hello from path!')
@app.route("/users/<string:user_id>")
def get_user(user_id):
    resp = client.get_item(
        TableName=USERS_TABLE,
        key={
            'userId': {'S': user_id}
        }
    )
    item = resp.get('Item')
    if not item:
        return jsonify({'error':'user does not exist'}),404
    return jsonify({
        'userId': item.get('userId').get('S'),
        'name': item.get('name').get('S')
    })

@app.route("/users", methods=["POST"])
def create_user():
    user_id = request.json.get('userId')
    name = request.json.get('name')
    if not user_id or not name:
        return jsonify({'error': 'Please provide userId and name'}), 400
 
    resp = client.put_item(
        TableName=USERS_TABLE,
        Item={
            'userId': {'S': user_id },
            'name': {'S': name }
        }
    )
 
    return jsonify({
        'userId': user_id,
        'name': name
    })