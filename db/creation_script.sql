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

CREATE TABLE AttachedFile (
	board_id DECIMAL(4),
	reply_id DECIMAL(18),
	filename NVARCHAR(256),
	fileTimestamp decimal(18),
	extension NVARCHAR(6),
	size DECIMAL(18),
	width DECIMAL(8),
	height DECIMAL(8),
	PRIMARY KEY (board_id, reply_id),
	FOREIGN KEY (board_id) REFERENCES Board(id)
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
	thread_number DECIMAL(18) NOT NULL,
    anon_name NVARCHAR(256),
    anon_id NVARCHAR(16),
    anon_country DECIMAL(4),
    creation_time DATETIME NOT NULL,
    content NVARCHAR(MAX),
    PRIMARY KEY (board_id, reply_id),
    FOREIGN KEY (board_id) REFERENCES Board(id),
	FOREIGN KEY (board_id, thread_number) REFERENCES Thread(board_id, thread_number),
    FOREIGN KEY (anon_country) REFERENCES Country(country_id),
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
	BEGIN
		INSERT INTO Country (country_name) VALUES (@country_name)
		SET @country_id = SCOPE_IDENTITY()
	END

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
			content, 
			thread_number
	) VALUES (
			@board_id,
			@reply_id,
			@anon_name,
			@anon_id,
			@country_id,
			@date,
			@content,
			@thread_number
	)
END
GO

-- MentionedReply insertion
CREATE PROCEDURE uspInsertMentionedReply(@board_id DECIMAL(4), @reply_id DECIMAL(18), @mentioned_reply_id DECIMAL(18))
AS
BEGIN
	BEGIN TRY
		INSERT INTO MentionedReply (board_id, reply_id, mentioned_reply_id) VALUES (@board_id, @reply_id, @mentioned_reply_id)
	END TRY
	BEGIN CATCH
		IF ERROR_NUMBER() = 2627 -- Replies can mention the same reply multiple times
		BEGIN
			RETURN 1
		END
		ELSE
		BEGIN
			;THROW
		END
	END CATCH
END
GO

-- Attached file insertion
CREATE PROCEDURE uspInsertAttachedFile(
			@board_id DECIMAL(4),
			@reply_id DECIMAL(18),
			@filename NVARCHAR(256),
			@fileTimestamp decimal(18),
			@extension NVARCHAR(6),
			@size DECIMAL(18),
			@width DECIMAL(8),
			@height DECIMAL(8))
AS
BEGIN
	INSERT INTO AttachedFile (
			board_id,
			reply_id,
			filename,
			fileTimestamp,
			extension,
			size,
			width,
			height)
	VALUES (
			@board_id,
			@reply_id,
			@filename,
			@fileTimestamp,
			@extension,
			@size,
			@width,
			@height
	)
END
GO

-- Get the threads with the highest amount of replies
CREATE PROCEDURE uspGetTopThreads(@board_name NVARCHAR(4), @TopN INT)
AS
BEGIN
	DECLARE @board_id NVARCHAR(4)
	SET @board_id = dbo.findBoardId(@board_name)

	SELECT TOP (@TopN)
		R.thread_number,
		COUNT(*) AS number_of_replies
	FROM Reply R
	WHERE R.board_id = @board_id
	GROUP BY R.thread_number
	ORDER BY 2 DESC
END
GO

-- Given a thread, get N amount of replies that have at least X words
CREATE PROCEDURE uspGetRepliesForThread
    @BoardName NVARCHAR(4),
    @ThreadNumber DECIMAL(18),
    @TopN INT,
    @MinWords INT
AS
BEGIN
    SELECT TOP (@TopN)
        R.content
    FROM Reply R
    WHERE
        R.board_id = dbo.findBoardId(@BoardName) AND
        R.thread_number = @ThreadNumber AND
        (SELECT COUNT(*) FROM STRING_SPLIT(R.content, ' ')) >= @MinWords;
END
GO

-- Create indexes

CREATE NONCLUSTERED INDEX IX_Reply_Country ON
	[dbo].[Reply] ([anon_country])

CREATE NONCLUSTERED INDEX IX_Reply_Board ON
	[dbo].[Reply] ([board_id], [thread_number])