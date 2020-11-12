SELECT 
		c.id,
		c.name
FROM categories  c
CREATE TABLE users (
  id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  first_name INTEGER NOT NULL,
  last_name INTEGER NOT NULL,
  email TEXT NOT NULL,
  password TEXT NOT NULL,
  activated TINYINT DEFAULT 1
);

INSERT INTO users VALUES (null, 'Jeff', 'Bridges', 'test1@test.com', 'password', 1)
INSERT INTO users VALUES (null, 'John', 'Malkovich', 'test1@test.com', 'password', 1)


CREATE TABLE categories (
  id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL
);

INSERT INTO categories VALUES (null, 'Test Category')
INSERT INTO categories VALUES (null, 'Test Category 2')



CREATE TABLE posts (
  id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  user_id REFERENCES users(id),
  creation_date INTEGER NOT NULL,
  category_id REFERENCES categories(id),
  subject TEXT NOT NULL,
  content TEXT NOT NULL
);

INSERT INTO posts VALUES (null, 1, 11022020, 1, 'Subject Text', 'Content Text');
INSERT INTO posts VALUES (null, 2, 11022020, 2, 'Subject Text 2', 'Content Text 2');

SELECT
  p.id,
  p.user_id,
  p.creation_date,
  p.category_id,
  p.subject,
  p.content,
  c.name category_name
FROM posts p
JOIN categories c
  ON p.category_id = c.id

CREATE TABLE comments (
  id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  user_id REFERENCES users(id),
  post_id REFERENCES posts(id),
  creation_date INTEGER NOT NULL,
  subject TEXT NOT NULL,
  content TEXT NOT NULL
);

INSERT INTO comments VALUES (null, 1, 1, 11022020, 'Comment Subject', 'Comment Content')
INSERT INTO comments VALUES (null, 2, 2, 11022020, 'Comment Subject 2', 'Comment Content 2')

        SELECT
            p.id,
            p.user_name,
            p.creation_date,
            p.category_id,
            p.subject,
            p.content
        FROM posts p



DROP TABLE posts

select * from users

UPDATE users
SET last_name = 'Goodman'
WHERE id = 4
