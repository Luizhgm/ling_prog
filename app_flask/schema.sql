DROP TABLE IF EXISTS options_user;
DROP TABLE IF EXISTS places;
DROP TABLE IF EXISTS user_infos;
DROP TABLE IF EXISTS account;
DROP TABLE IF EXISTS post; 
DROP TABLE IF EXISTS options_post;

CREATE TABLE options_user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  type TEXT UNIQUE NOT NULL
);

CREATE TABLE places(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  adress TEXT NOT NULL,
  about TEXT
);

CREATE TABLE user_infos(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  CPF varchar(10) UNIQUE CHECK (LENGTH(CPF)=10),
  name TEXT NOT NULL,
  place_id INTEGER NOT NULL,
  email TEXT,  
    
  FOREIGN KEY (place_id) REFERENCES places (id)  
);
    
    
CREATE TABLE account (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  options_id INTEGER NOT NULL,
  activate Boolean NOT NULL DEFAULT FALSE,
  
  FOREIGN KEY (user_id) REFERENCES user_info (id)
  FOREIGN KEY (options_id) REFERENCES options_user (id)
);


CREATE TABLE options_post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  type TEXT UNIQUE NOT NULL,
  about TEXT
  

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
  place_id INTEGER NOT NULL DEFAULT 1,
    
  FOREIGN KEY (place_id) REFERENCES places (id),
  FOREIGN KEY (author_id) REFERENCES user_infos (id),
  FOREIGN KEY (options_id) REFERENCES options_post (id)
    
);

INSERT INTO places(name, adress ,about) VALUES ("NONE","NONE","para preenchimentos e não precisar preencher em lugar default");
INSERT INTO user_infos(name, place_id, email, CPF) VALUES ("JANUS", 1, "JANUS@gmail.com", "0000000000");
INSERT INTO options_user (type) VALUES ("admin");
INSERT INTO options_user (type) VALUES ("criador de vaga");
INSERT INTO options_user (type) VALUES ("pedidor de vaga");