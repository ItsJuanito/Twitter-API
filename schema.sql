Pramga foreign_keys=On
BEGIN TRANSACTION;

DROP TABLE IF EXISTS users;
CREATE TABLE users (
    username VARCHAR(25) PRIMARY KEY,
    email VARCHAR(45),
    password VARCHAR(25),
    bio VARCHAR(155)
);

DROP TABLE IF EXISTS tweets;
CREATE TABLE tweets (
    id INTEGER PRIMARY KEY,
    text VARCHAR(255),
    timestamp DATE,
    author VARCHAR(25),
    FOREIGN KEY (author) REFERENCES users(username)
);

DROP TABLE IF EXISTS followerlist;
CREATE TABLE followerlist (
    follower VARCHAR(25),
    username VARCHAR(25),
    FOREIGN KEY (username) REFERENCES users(username)
);

INSERT INTO users(username, email, password, bio) VALUES ('blaster02', 'blaster02@tomorrowland.com', 'iblast92', 'This is my bio!');

COMMIT;