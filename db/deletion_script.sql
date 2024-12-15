USE BoardCrawler

-- Drop tables

DROP TABLE MentionedReply
DROP TABLE Reply
DROP TABLE Thread
DROP TABLE Country
DROP TABLE Board

-- Drop functions

DROP FUNCTION dbo.findBoardId

-- Drop stored procedures

DROP PROCEDURE uspInsertBoard
DROP PROCEDURE uspInsertThread
DROP PROCEDURE uspInsertCountry
DROP PROCEDURE uspInsertReply
DROP PROCEDURE uspInsertMentionedReply