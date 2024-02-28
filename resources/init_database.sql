CREATE DATABASE site_consciencia_negra;
USE site_consciencia_negra;

CREATE TABLE users(
	id INT PRIMARY KEY AUTO_INCREMENT,
	name VARCHAR(100) UNIQUE,
	password VARCHAR(60),
	salt VARCHAR(60)
);

CREATE TABLE comments(
	id INT PRIMARY KEY AUTO_INCREMENT,
	user_id INT NOT NULL,
	type_id INT NOT NULL,
	type VARCHAR(20) NOT NULL,
	text TEXT NOT NULL,
	date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(id),
	CONSTRAINT check_type CHECK (type IN ('photos', 'movies', 'events')),
    UNIQUE (id, type, type_id)
);

CREATE TABLE movies(
	id INT PRIMARY KEY AUTO_INCREMENT,
	image_url text not null,
	title VARCHAR(100) UNIQUE NOT NULL,
	sinopse TEXT,
	date DATE,
	duration TIME,
	classification SMALLINT
);

CREATE TABLE events (
	id INT PRIMARY KEY AUTO_INCREMENT,	
    title VARCHAR(100),
    description VARCHAR(100),
    date DATE,
    local VARCHAR(100)
);

CREATE TABLE photos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    image_url VARCHAR(255) NOT NULL,
    caption TEXT,
    date DATE
);