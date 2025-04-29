-- Populating the AUTHORS table
INSERT INTO AUTHORS (FirstName, LastName) VALUES
('Jane', 'Doe'),
('John', 'Smith'),
('Emily', 'Carter'),
('David', 'Wilson'),
('Sophia', 'Garcia'),
('Charles', 'Lee'),
('Olivia', 'Martinez'),
('Daniel', 'Hall'),
('Isabella', 'Young'),
('Ethan', 'Wright');

-- Populating the REVIEWERS table
INSERT INTO REVIEWERS (FirstName, LastName) VALUES
('Robert', 'Jones'),
('Olivia', 'Brown'),
('William', 'Davis'),
('Ava', 'Miller'),
('James', 'Wilson'),
('Mia', 'Moore'),
('Noah', 'Taylor'),
('Amelia', 'Anderson'),
('Lucas', 'Thomas'),
('Harper', 'Jackson');

-- Populating the PAPERS table
INSERT INTO PAPERS (Title, AuthorID, ReviewerID) VALUES
('Novel Approaches in Machine Learning', 1, 2),
('The Impact of Climate Change on Coastal Regions', 3, 1),
('A Study of Quantum Entanglement', 2, 4),
('Exploring Deep Learning Architectures', 1, 3),
('The Role of Social Media in Political Discourse', 4, 5),
('Advancements in Natural Language Processing', 5, 2),
('Sustainable Energy Solutions for Urban Areas', 3, NULL),
('Understanding Black Holes and Their Properties', 2, 1),
('The Ethics of Artificial Intelligence', 4, 3),
('New Methods for Data Visualization', 5, 4),
('The Future of Autonomous Vehicles', 6, 7),
('Understanding the Human Microbiome', 7, 6),
('Advances in Renewable Energy Technology', 8, 9),
('The Impact of Globalization on Local Cultures', 9, 8),
('Artificial Intelligence in Healthcare Diagnostics', 10, 10),
('Exploring the Mysteries of Dark Matter', 6, 9),
('The Psychology of Online Learning', 7, 7),
('Developments in Nanotechnology', 8, 6),
('The History of Ancient Civilizations', 9, 10),
('Machine Learning for Financial Forecasting', 10, 8),
('A Comparative Study of Programming Languages', 1, 11),
('The Art and Science of Photography', 3, 12),
('The Benefits of Mindfulness Meditation', 5, 13),
('Exploring Different Styles of Jazz Music', 2, 14),
('The Impact of Social Media on Teen Mental Health', 4, 15);