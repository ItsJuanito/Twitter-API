from urllib import response
from flask import Blueprint
import sqlite3
from flask import g, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

users_api = Blueprint('users', __name__, url_prefix='/users')

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

# works
@users_api.route('/')
def main():
    message = '''End routes:
    /users - to create a user
    /users/<username>/<password> - to authenticate user
    /users/update - to edit user bio
    /users/all - to get all of the users
    /users/followers/add/<username> - add a follower
    /users/followers/remove/<username> - remove a follower
    /users/followers/all/<username> - get all followers from that user'''
    return message
# works
@users_api.route("/create", methods=['POST'])
def createUser():
    try :
        params = request.get_json()
        username = params['username']
        email = params['email']
        password = params['password']
        hashed_password = generate_password_hash(password)
        bio = params['bio']

        db = get_db()
        query_db("INSERT INTO users(username, email, password, bio) VALUES (?, ?, ?, ?)", (username, email, hashed_password, bio))
        db.commit()
        response = jsonify({'status' : 'created'})
        response.code = 201
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response
    except Exception:
        response = jsonify({'status' : 'Bad request'})
        response.code = 400
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response
# works
@users_api.route('/<username>/<password>', methods=['GET'])
def authenticateUser(username, password):
    try:
        user = query_db('SELECT * FROM users WHERE username = ?;', (username, ))
        pwd = user[0]['password']
        check = check_password_hash(pwd, password)
        if check == True:
            response = jsonify({'status' : 'Authorized'})
            response.code = 200
            response.headers["Content-Type"] = "application/json; charset=utf-8"
            return response
        else:
            response = jsonify({'message' : 'Authenticate'})
            response.code = 401
            response.headers["Content-Type"] = "application/json; charset=utf-8"
    except Exception:
        response = jsonify({'status' : 'Bad request'})
        response.code = 400
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response
# works
@users_api.route('/update', methods=['PUT'])
def editBio():
    try:
        params = request.get_json()
        bio = params['bio']
        username = params['username']
        db = get_db()
        query_db('UPDATE users SET bio=? WHERE username=?;', (bio, username))
        db.commit()
        response = jsonify({ 'status' : 'Updated' })
        response.code = 201
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response
    except Exception:
        response = jsonify({'status' : 'Bad request'})
        response.code = 400
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response
# works
@users_api.route('/all', methods=['GET'])
def usersAll():
    all_users = query_db("SELECT * FROM users")
    return jsonify(all_users)
# works
@users_api.route('/followers/add/<username>', methods=['POST'])
def addFollower(username):
    try:
        params = request.get_json()
        follower = params['follower']
        db = get_db()
        query_db('INSERT INTO followerlist(follower, username) VALUES (?, ?);', (follower, username))
        db.commit()
        response = jsonify({'status' : 'user added'})
        response.code = 201
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response
    except Exception:
        response = jsonify({'status' : 'bad request'})
        response.code = 400
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response

@users_api.route('/followers/remove/<username>', methods=['DELETE'])
def removeFollower(username):
    try:
        params = request.get_json()
        follower = params['follower']
        db = get_db()
        query_db('DELETE FROM followerlist WHERE follower=? AND username=?;', (follower, username))
        db.commit()
        response = jsonify({'status' : 'accepted'})
        response.code = 202
        response.headers["Conetent-Type"] = "application/json; charset=utf-8"
        return response
    except Exception:
        response = jsonify({'status' : 'bad request'})
        response.code = 400
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response
# works
@users_api.route('/followers/all/<username>', methods=['GET'])
def followersAll(username):
    follower_list = query_db('SELECT follower FROM followerlist WHERE username=?;', (username, ))
    return jsonify(follower_list)
