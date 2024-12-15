CREATE DATABASE BoardCrawler

USE BoardCrawler

-- Create tables

CREATE TABLE Board (
    id DECIMAL(4) PRIMARY KEY IDENTITY(1,1),
    board_name NVARCHAR(10) NOT NULL,
    title NVARCHAR(50) NOT NULL
)

CREATE TABLE Country (
    country_id DECIMAL(4) PRIMARY KEY IDENTITY(1,1),
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
    content NVARCHAR(MAX),
	thread_number DECIMAL(18) NOT NULL,
    PRIMARY KEY (board_id, reply_id),
    FOREIGN KEY (board_id) REFERENCES Board(id),
	FOREIGN KEY (board_id, thread_number) REFERENCES Thread(board_id, thread_number),
    FOREIGN KEY (anon_country) REFERENCES Country(country_id)
)

CREATE TABLE MentionedReply (
    board_id DECIMAL(4),
    reply_id DECIMAL(18),
    mentioned_reply_id DECIMAL(18),
    PRIMARY KEY (board_id, reply_id, mentioned_reply_id),
    FOREIGN KEY (board_id, reply_id) REFERENCES Reply(board_id, reply_id),
    FOREIGN KEY (board_id, mentioned_reply_id) REFERENCES Reply(board_id, reply_id)
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
GO

-- Thread insertion
CREATE PROCEDURE uspInsertThread(@board_id DECIMAL(4), @thread_number DECIMAL(18), @title NVARCHAR(256)) AS
BEGIN
	INSERT INTO Thread (board_id, thread_number, title) VALUES (@board_id, @thread_number, @title)
END
GO

-- Country insertion
CREATE PROCEDURE uspInsertCountry(@country_name NVARCHAR(256)) 
AS
BEGIN
	
	DECLARE @country_id DECIMAL(4)
	SET @country_id = (SELECT c.country_id FROM Country c WHERE c.country_name = @country_name)

	IF @country_id IS NULL
		INSERT INTO Country (country_name) VALUES (@country_name)
		SET @country_id = SCOPE_IDENTITY()
	
	RETURN @country_id
END
GO

-- Reply insertion
CREATE PROCEDURE uspInsertReply(
				@board_id DECIMAL(4),
				@reply_id DECIMAL(18),
				@anon_name NVARCHAR(256),
				@anon_id NVARCHAR(16),
				@anon_country_name NVARCHAR(256),
				@timestamp INT,
				@filename NVARCHAR(256),
				@content NVARCHAR(MAX),
				@thread_number DECIMAL(18)) AS
BEGIN
	DECLARE @country_id DECIMAL(4)
	DECLARE @date DATETIME

	SET @date = DATEADD(S, @timestamp, '1970-01-01')

	IF @anon_country_name IS NOT NULL
	BEGIN
		EXEC @country_id = dbo.uspInsertCountry @anon_country_name
	END

	INSERT INTO Reply (
			board_id, 
			reply_id, 
			anon_name, 
			anon_id, 
			anon_country, 
			creation_time, 
			filename, 
			content, 
			thread_number
	) VALUES (
			@board_id,
			@reply_id,
			@anon_name,
			@anon_id,
			@anon_country_name,
			@date,
			@filename,
			@content,
			@thread_number
	)
END
GO

-- MentionedReply insertion
CREATE PROCEDURE uspInsertMentionedReply(@board_id DECIMAL(4), @reply_id DECIMAL(18), @mentioned_reply_id DECIMAL(18))
AS
BEGIN
	INSERT INTO MentionedReply (board_id, reply_id, mentioned_reply_id) VALUES (@board_id, @reply_id, @mentioned_reply_id)
END
GO