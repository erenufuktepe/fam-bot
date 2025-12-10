
CREATE SCHEMA IF NOT EXISTS fambot;

CREATE TABLE IF NOT EXISTS fambot.users (
    id BIGINT  PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    is_allowed BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS fambot.appointments (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id BIGINT NOT NULL,
    title VARCHAR(200) NOT NULL,
    start_datetime TIMESTAMP NOT NULL,
    location VARCHAR(200),
    note TEXT,
    FOREIGN KEY (user_id) REFERENCES fambot.users(id)
);

CREATE TABLE IF NOT EXISTS fambot.birthdays (
    person_name VARCHAR(100) PRIMARY KEY NOT NULL,
    user_id BIGINT NOT NULL,
    month INT NOT NULL,  -- 1-12
    day INT NOT NULL,     -- 1-31
    FOREIGN KEY (user_id) REFERENCES fambot.users(id)
);

CREATE TABLE IF NOT EXISTS fambot.tasks (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id BIGINT NOT NULL,
    chat_id BIGINT NOT NULL,
    task_name VARCHAR(200) NOT NULL,
    cron_expression VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL,
    notes TEXT,
    FOREIGN KEY (user_id) REFERENCES fambot.users(id)
);


CREATE TABLE IF NOT EXISTS fambot.shopping_items (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id BIGINT NOT NULL,
    item_name VARCHAR(200) NOT NULL,
    quantity INT,
    note TEXT,
    created_datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES fambot.users(id)
);


DROP TABLE IF EXISTS fambot.appointments;
DROP TABLE IF EXISTS fambot.birthdays;
DROP TABLE IF EXISTS fambot.tasks;
DROP TABLE IF EXISTS fambot.shopping_items; 
DROP TABLE IF EXISTS fambot.users;


SELECT * FROM appointments