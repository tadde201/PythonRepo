CREATE DATABASE CareerMatch;

USE CareerMatch;

CREATE TABLE Jobs
(
    JobID INT IDENTITY PRIMARY KEY,
    Title VARCHAR(200),
    Company VARCHAR(200),
    Description VARCHAR(MAX),
    Location VARCHAR(100),
    MatchScore INT,
    CreatedDate DATETIME DEFAULT GETDATE()
);
select * from Jobs
