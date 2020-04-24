CREATE TABLE users(
username CHAR(50) PRIMARY KEY,
password_hash VARCHAR(225) NOT NULL,
password_salt VARCHAR(10) NOT NULL,
created_on TIMESTAMP NOT NULL,
last_password_changed TIMESTAMP,
last_login TIMESTAMP
);

CREATE TABLE userextended(
    username CHAR(50) PRIMARY KEY REFERENCES users(username),
    first_name VARCHAR(50) NOT NULL,
    second_name VARCHAR(40),
    icon_photo_path VARCHAR(70) ,
    user_description VARCHAR(225) ,
	institution VARCHAR(40),
    teacher BOOLEAN,
    email VARCHAR(30),
    last_active TIMESTAMP,
	upload_folder VARCHAR(30)
	);

