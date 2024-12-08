CREATE DATABASE BoardCrawler

USE BoardCrawler

CREATE TABLE Board (
    id DECIMAL(4) PRIMARY KEY IDENTITY(1,1),
    board_name NVARCHAR(10) NOT NULL,
    title NVARCHAR(50) NOT NULL
)

CREATE TABLE Thread (
    board_id DECIMAL(4),
    thread_number DECIMAL(18),
    title NVARCHAR(256),
    timestamp DATETIME NOT NULL,
    PRIMARY KEY (board_id, thread_number),
    FOREIGN KEY (board_id) REFERENCES Board(id)
)

CREATE TABLE Countries (
    country_id DECIMAL(4) PRIMARY KEY,
    country_name NVARCHAR(256) NOT NULL
)

CREATE TABLE Reply (
    board_id DECIMAL(4) NOT NULL,
    reply_id DECIMAL(18) NOT NULL,
    anon_name NVARCHAR(256),
    anon_id NVARCHAR(16),
    anon_country DECIMAL(4),
    timestamp DATETIME NOT NULL,
    filename NVARCHAR(256),
    replies_mentioned DECIMAL(18),
    content NVARCHAR(MAX),
    PRIMARY KEY (board_id, reply_id),
    FOREIGN KEY (board_id) REFERENCES Board(id),
    FOREIGN KEY (anon_country) REFERENCES Countries(country_id)
)

CREATE TABLE ReplyMentions (
    board_id DECIMAL(4),
    reply_id DECIMAL(18),
    mentioned_reply DECIMAL(18),
    PRIMARY KEY (board_id, reply_id, mentioned_reply),
    FOREIGN KEY (board_id, reply_id) REFERENCES Reply(board_id, reply_id),
    FOREIGN KEY (board_id, mentioned_reply) REFERENCES Reply(board_id, reply_id)
)
