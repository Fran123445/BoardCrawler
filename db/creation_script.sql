CREATE DATABASE BoardCrawler

USE BoardCrawler

-- Create tables

CREATE TABLE Board (
    id DECIMAL(4) PRIMARY KEY IDENTITY(1,1),
    board_name NVARCHAR(10) NOT NULL,
    title NVARCHAR(50) NOT NULL
)

CREATE TABLE Countries (
    country_id DECIMAL(4) PRIMARY KEY,
    country_name NVARCHAR(256) NOT NULL
)


CREATE TABLE Thread (
    board_id DECIMAL(4),
    thread_number DECIMAL(18),
    title NVARCHAR(256),
    PRIMARY KEY (board_id, thread_number),
    FOREIGN KEY (board_id) REFERENCES Board(id),
)

CREATE TABLE Reply (
    board_id DECIMAL(4),
    reply_id DECIMAL(18),
    anon_name NVARCHAR(256),
    anon_id NVARCHAR(16),
    anon_country DECIMAL(4),
    creation_time DATETIME NOT NULL,
    filename NVARCHAR(256),
    replies_mentioned DECIMAL(18),
    content NVARCHAR(MAX),
	thread_number DECIMAL(18) NOT NULL,
    PRIMARY KEY (board_id, reply_id),
    FOREIGN KEY (board_id) REFERENCES Board(id),
	FOREIGN KEY (board_id, thread_number) REFERENCES Thread(board_id, thread_number),
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
GO

-- Create functions

-- Find board by name
CREATE FUNCTION findBoardId(@board_name NVARCHAR(10))
RETURNS DECIMAL(4)
AS
BEGIN
	RETURN (SELECT b.id FROM Board b WHERE b.board_name = @board_name)
END
GO

-- Create store procedures

-- Board insertion
CREATE PROCEDURE uspInsertBoard(@board_name NVARCHAR(10), @board_title NVARCHAR(50)) AS
BEGIN
	IF dbo.findBoardId(@board_name) IS NULL
	BEGIN
		INSERT INTO Board (board_name, title) VALUES (@board_name, @board_title)
		RETURN 0 -- all good
	END

	RETURN 1 -- the board is already in the db
END

CREATE PROCEDURE uspInsertThread(@board_name NVARCHAR(10), @thread_number DECIMAL(18), @title NVARCHAR(256)) AS
BEGIN
	DECLARE @board_id DECIMAL(4)
	SET @board_id = dbo.findBoardId(@board_name)

	INSERT INTO Thread (board_id, thread_number, title) VALUES (@board_id, @thread_number, @title)
END