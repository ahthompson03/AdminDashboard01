-- Delete existing data from tables to ensure a clean slate
-- MySQL uses TRUNCATE for faster deletion (optional, if you don't need rollback)
-- Disable foreign key checks to allow truncation in any order
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE PAPER_REVIEWERS;
TRUNCATE TABLE TRACKS;
TRUNCATE TABLE PAPERS;
TRUNCATE TABLE AUTHORS;
TRUNCATE TABLE REVIEWERS;
TRUNCATE TABLE User;
SET FOREIGN_KEY_CHECKS = 1;

-- Insert sample data into AUTHORS table
INSERT INTO AUTHORS (AuthorID, FirstName, LastName) VALUES
    (1, 'John', 'Smith'),
    (2, 'Jane', 'Doe'),
    (3, 'Robert', 'Jones'),
    (4, 'Emily', 'Brown'),
    (5, 'Michael', 'Davis'),
    (6, 'Jessica', 'Wilson'),
    (7, 'David', 'Garcia'),
    (8, 'Linda', 'Rodriguez'),
    (9, 'Christopher', 'Williams'),
    (10, 'Angela', 'Martinez');

-- Insert sample data into REVIEWERS table
INSERT INTO REVIEWERS (ReviewerID, FirstName, LastName, ReviewerEmail) VALUES
    (1, 'Alice', 'Johnson', 'alice.johnson@example.com'),
    (2, 'Bob', 'Williams', 'bob.williams@example.com'),
    (3, 'Charlie', 'Brown', 'charlie.brown@example.com'),
    (4, 'David', 'Miller', 'david.miller@example.com'),
    (5, 'Eve', 'Wilson', 'eve.wilson@example.com'),
    (6, 'Frank', 'Garcia', 'frank.garcia@example.com'),
    (7, 'Grace', 'Martinez', 'grace.martinez@example.com'),
    (8, 'Henry', 'Robinson', 'henry.robinson@example.com'),
    (9, 'Isabella', 'Clark', 'isabella.clark@example.com'),
    (10, 'Jack', 'Lopez', 'jack.lopez@example.com'),
    (11, 'Katherine', 'Young', 'katherine.young@example.com'),
    (12, 'Liam', 'King', 'liam.king@example.com');

-- Insert sample data into PAPERS table
INSERT INTO PAPERS (PaperID, Title, AuthorID) VALUES
    (1, 'A Study of Algorithms', 1),
    (2, 'The Future of AI', 2),
    (3, 'Data Mining Techniques', 1),
    (4, 'Machine Learning Basics', 3),
    (5, 'Deep Learning Architectures', 2),
    (6, 'Natural Language Processing', 4),
    (7, 'Computer Vision Advances', 5),
    (8, 'Quantum Computing Explained', 1),
    (9, 'Blockchain Technology', 3),
    (10, 'Cybersecurity Threats', 4),
    (11, 'Advanced Database Systems', 5),
    (12, 'Software Engineering Principles', 1),
    (13, 'Web Development Frameworks', 2),
    (14, 'Mobile Application Development', 3),
    (15, 'Cloud Computing Concepts', 4),
    (16, 'Big Data Analytics', 5),
    (17, 'Internet of Things (IoT)', 1),
    (18, 'Human-Computer Interaction', 2),
    (19, 'Robotics and Automation', 3),
    (20, 'Ethical Hacking Techniques', 4);

-- Insert sample data into User table
INSERT INTO User (id, username, password) VALUES
    (1, 'john_smith', 'password123'),
    (2, 'jane_doe', 'securepass'),
    (3, 'emily_brown', 'password456'),
    (4, 'michael_davis', 'securepass789'),
    (5, 'jessica_wilson', 'password1011'),
    (6, 'david_garcia', 'securepass1213'),
    (7, 'linda_rodriguez', 'password1415'),
    (8, 'christopher_williams', 'securepass1617');