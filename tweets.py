from urllib import response
from flask import Blueprint
import sqlite3
from flask import g, request, jsonify
from datetime import datetime

tweets_api = Blueprint('tweets', __name__, url_prefix='/tweets')

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value) for idx, value in enumerate(row))

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('users.db')
        db.row_factory = make_dicts
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@tweets_api.route('/', methods=['GET'])
def home():
    message = '''End Routes:
    /tweets/<username> - post a tweet
    /tweets/delete/<username> - delete a tweet
    /tweets/timeline/public - get the public timeline
    /tweets/timeline/user/<username> - get the timeline of a specific user
    /tweets/timeline/home/<username> - get the home timeline
    '''
    return message

@tweets_api.route('/<username>', methods=['POST'])
def createPost(username):
    try:
        params = request.get_json()
        text = params['text']
        now = datetime.now()
        timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
        db = get_db()
        query_db('INSERT INTO tweets(text, timestamp, author) VALUES (?, ?, ?);', (text, timestamp, username))
        db.commit()
        response = jsonify({'status' : 'created'})
        response.code = 201
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response
    except Exception:
        response = jsonify({'status' : 'bad request'})
        response.code = 400
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response

@tweets_api.route('/delete/<username>', methods=['DELETE'])
def deleteTweet(username):
    try:
        params = request.get_json()
        tweet_id = params['id']
        db = get_db()
        query_db('DELETE FROM tweets WHERE id=? AND author=?;', (tweet_id, username))
        db.commit()
        response = jsonify({'status' : 'accepted'})
        response.code = 202
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response
    except Exception:
        response = jsonify({'status' : 'bad request'})
        response.code = 400
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response

@tweets_api.route('/timeline/<username>', methods=['GET'])
def getUserTimeline(username):
    try:
        response = query_db('SELECT text, timestamp FROM tweets WHERE author=?;', (username, ))
        return jsonify(response)
    except Exception:
        response = jsonify({'status' : 'bad request'})
        response.code = 400
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response

@tweets_api.route('/timeline/public', methods=['GET'])
def getPublicTimeline():
    try:
        response = query_db('SELECT text, timestamp, author FROM tweets ORDER BY timestamp DESC LIMIT 25;')
        return jsonify(response)
    except Exception:
        response = jsonify({'status' : 'bad request'})
        response.code = 400
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response

@tweets_api.route('/timeline/home/<username>', methods=['GET'])
def getHomeTimeline(username):
    try:
        response = query_db('SELECT text, timestamp, author FROM tweets WHERE auther IN (SELECT follower FROM followerlist WHERE username=?) ORDER BY timestamp DESC LIMIT 25;', (username, ))
        return jsonify(response)
    except Exception:
        response = jsonify({'status' : 'bad request'})
        response.code = 400
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response