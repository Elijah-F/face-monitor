CREATE DATABASE IF NOT EXISTS face_monitor DEFAULT CHARSET utf8 COLLATE utf8_general_ci;
use face_monitor;

CREATE TABLE IF NOT EXISTS user_info (
    phone VARCHAR(11) PRIMARY KEY NOT NULL,
    name VARCHAR(256),
    passwd VARCHAR(32),
    register_timestamp TIMESTAMP NOT NULL DEFAULT current_timestamp()
);

/* CREATE TABLE IF NOT EXISTS room_info ( */
/*     id VARCHAR(10) PRIMARY KEY NOT NULL, */
/*     is_using BOOLEAN, */
/*     create_time TIMESTAMP NOT NULL DEFAULT current_timestamp() */
/* ) */
