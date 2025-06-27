CREATE TABLE IF NOT EXISTS login (
    login_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255),
    password VARCHAR(255),
    usertype VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS authority (
    authority_id INT PRIMARY KEY AUTO_INCREMENT,
    login_id INT,
    authority_name VARCHAR(255),
    district VARCHAR(255),
    place VARCHAR(255),
    phone VARCHAR(255),
    email VARCHAR(255),
    status VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS user (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    login_id INT,
    fname VARCHAR(255),
    lname VARCHAR(255),
    district VARCHAR(255),
    place VARCHAR(255),
    phone VARCHAR(255),
    email VARCHAR(255),
    latitude VARCHAR(255),
    longitude VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS complaints (
    complaints_id INT PRIMARY KEY AUTO_INCREMENT,
    sender_id(login_id - user/authority) VARCHAR(255),
    title VARCHAR(255),
    description VARCHAR(255),
    reply VARCHAR(255),
    date VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS authority_land_slide_report (
    authority_report_id INT PRIMARY KEY AUTO_INCREMENT,
    authority_id INT,
    place_name VARCHAR(255),
    latitude VARCHAR(255),
    longitude VARCHAR(255),
    date VARCHAR(255),
    time VARCHAR(255),
    status VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS emergency_notification (
    emergency_notification_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255),
    description VARCHAR(255),
    date VARCHAR(255),
    status VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS helpline_number (
    helpline_number_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255),
    number VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS user_land_slide_report (
    user_report_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    place VARCHAR(255),
    latitude VARCHAR(255),
    longitude VARCHAR(255),
    date VARCHAR(255),
    time VARCHAR(255),
    status VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS family_friends_number (
    family_friend_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    name VARCHAR(255),
    number VARCHAR(255)
);

