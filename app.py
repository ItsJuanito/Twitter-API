from flask import Flask
from users import users_api
from tweets import tweets_api

app = Flask(__name__)
'''
functions needed for api:
- create user
- authenticate user
- edit user bio
- add follower
- remove follower
- get all users
- get follower list

py -3 -m venv venv
venv\Scripts\activate

pip install Flask
pip install werkzeug
'''
@app.route('/')
def main():
    return 'Hello World!'

if __name__ == "__main__":

    app.register_blueprint(users_api)
    app.register_blueprint(tweets_api)

    app.run()