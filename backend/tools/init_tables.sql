CREATE DATABASE IF NOT EXISTS face_monitor DEFAULT CHARSET utf8 COLLATE utf8_general_ci;
use face_monitor;

CREATE TABLE IF NOT EXISTS user_info (
    phone VARCHAR(11) PRIMARY KEY NOT NULL,
    name VARCHAR(256),
    passwd VARCHAR(32),
    register_timestamp TIMESTAMP NOT NULL DEFAULT current_timestamp()
);

CREATE TABLE IF NOT EXISTS history (
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    job_id VARCHAR(256) NOT NULL,
    phone VARCHAR(11) NOT NULL,
    meeting_number_str VARCHAR(16) NOT NULL,
    sleepy BOOLEAN NOT NULL COMMENT '是否检测到睡意',
    detected_face BOOLEAN NOT NULL COMMENT '是否探测到人脸',
    smile BOOLEAN NOT NULL COMMENT '是否检测到微笑',
    speak BOOLEAN NOT NULL COMMENT '是否检测到讲话',
    x FLOAT NOT NULL COMMENT '人脸的x坐标',
    y FLOAT NOT NULL COMMENT '人脸的y坐标',
    z FLOAT NOT NULL COMMENT '人脸的z坐标',
    insert_time TIMESTAMP NOT NULL DEFAULT current_timestamp()
);

CREATE TABLE IF NOT EXISTS image_history (
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    job_id VARCHAR(256) NOT NULL,
    type VARCHAR(16) NOT NULL,
    image_data TEXT NOT NULL
);
