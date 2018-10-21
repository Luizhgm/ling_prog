DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS options_post;
DROP TABLE IF EXISTS options_user;

CREATE TABLE options_user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  type TEXT UNIQUE NOT NULL
);

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  options_id INTEGER NOT NULL,
  activate Boolean NOT NULL,
  
  FOREIGN KEY (options_id) REFERENCES options_user (id)
);



CREATE TABLE options_post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  type TEXT UNIQUE NOT NULL,
  link TEXT
  

);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  options_id INTEGER NOT NULL,
  places INTEGER NOT NULL DEFAULT 1,
  money FLOAT NOT NULL DEFAULT 0,
  hours TIME NOT NULL DEFAULT 0,
  link TEXT,
  body TEXT,
  
  FOREIGN KEY (author_id) REFERENCES user (id),
  FOREIGN KEY (options_id) REFERENCES options_post (id)
    
);


INSERT INTO options_user (type) VALUES ("admin");
INSERT INTO options_user (type) VALUES ("criador de vaga");
INSERT INTO options_user (type) VALUES ("pedidor de vaga");