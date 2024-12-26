USE BoardCrawler

-- Drop tables

DROP TABLE MentionedPost
DROP TABLE Post
DROP TABLE Thread
DROP TABLE AttachedFile
DROP TABLE Country
DROP TABLE Board

-- Drop functions

DROP FUNCTION dbo.findBoardId

-- Drop stored procedures

DROP PROCEDURE uspInsertBoard
DROP PROCEDURE uspInsertThread
DROP PROCEDURE uspInsertCountry
DROP PROCEDURE uspInsertPost
DROP PROCEDURE uspInsertMentionedPost
DROP PROCEDURE uspInsertAttachedFile
DROP PROCEDURE uspGetPostsForThread
DROP PROCEDURE uspGetTopThreads