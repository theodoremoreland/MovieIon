CREATE TABLE users(
  user_id SERIAL PRIMARY KEY 
  , username VARCHAR(5) NOT NULL
  , watchlist text[]
);

BEGIN TRANSACTION;
INSERT INTO users(username) VALUES ('user1');
INSERT INTO users(username) VALUES ('user2');
INSERT INTO users(username) VALUES ('user3');
INSERT INTO users(username) VALUES ('user4');
INSERT INTO users(username) VALUES ('user5');
INSERT INTO users(username) VALUES ('user6');
COMMIT;