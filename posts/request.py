import sqlite3
import json
from models import Post, User, Category

def get_all_posts():
    with sqlite3.connect("./mammoth_cave.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id,
            p.creation_date,
            p.category_id,
            p.subject,
            p.content,
            u.id,
            u.first_name,
            u.last_name,
            u.email,
            u.password,
            c.id,
            c.name
        FROM posts p
        JOIN users u
            ON u.id = p.user_id
        JOIN categories c
            ON c.id = p.category_id
        ORDER BY p.creation_date DESC
        """)

        posts = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            post = Post(row['id'], row['user_id'], row['creation_date'], row['category_id'], row['subject'], row['content'])
            user = User(row['user_id'], row['first_name'], row['last_name'], row['email'], row['password'])
            category = Category(row['category_id'], row['name'])

            post.user = user.__dict__

            post.category = category.__dict__

            posts.append(post.__dict__)

    return json.dumps(posts)

def get_post_by_id(id):
    with sqlite3.connect("./mammoth_cave.db") as conn:
        conn.row_factory = sqlite3.Row

        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id,
            p.creation_date,
            p.category_id,
            p.subject,
            p.content,
            u.id,
            u.first_name,
            u.last_name,
            u.email,
            u.password,
            c.id,
            c.name
        FROM posts p
        JOIN users u
            ON u.id = p.user_id
        JOIN categories c
            ON c.id = p.category_id
        WHERE p.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()

        post = Post(data['id'], data['user_id'], data['creation_date'], data['category_id'], data['subject'], data['content'])
        user = User(data['user_id'], data['first_name'], data['last_name'], data['email'], data['password'])
        category = Category(data['category_id'], data['name'])

        post.user = user.__dict__

        post.category = category.__dict__

        return json.dumps(post.__dict__)

def create_post(new_post):
    with sqlite3.connect('./mammoth_cave.db') as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO posts
            (user_id, creation_date, category_id, subject, content)
        VALUES 
            (?, ?, ?, ?, ?);
        """, (int(new_post['user_id']), new_post['creation_date'], int(new_post['category_id']), new_post['subject'], new_post['content'], ))

        id = db_cursor.lastrowid

        new_post['id'] = id

    return json.dumps(new_post)

def delete_post(id):
    with sqlite3.connect("./mammoth_cave.db") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        DELETE FROM posts
        WHERE id = ?
        """, (id, ))

def get_posts_by_user(user_id):
    with sqlite3.connect("./mammoth_cave.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id,
            p.creation_date,
            p.category_id,
            p.subject,
            p.content,
            u.id,
            u.first_name,
            u.last_name,
            u.email,
            u.password,
            c.id,
            c.name
        FROM posts p
        JOIN users u
            ON u.id = p.user_id
        JOIN categories c
            ON c.id = p.category_id
        WHERE u.id = ?
        """, ( user_id, ))

        posts = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            post = Post(row['id'], row['user_id'], row['creation_date'], row['category_id'], row['subject'], row['content'], )
            user = User(row['user_id'], row['first_name'], row['last_name'], row['email'], row['password'], )
            category = Category(row['category_id'], row['name'])

            post.user = user.__dict__

            post.category = category.__dict__

            posts.append(post.__dict__)

    return json.dumps(posts)

def update_post(id, new_post):
    with sqlite3.connect("./mammoth_cave.db") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        UPDATE posts
            SET
                user_id = ?,
                creation_date = ?,
                category_id = ?,
                subject = ?,
                content = ?
        WHERE id = ?
        """, (int(new_post['user_id']), new_post['creation_date'],
              int(new_post['category_id']), new_post['subject'],
              new_post['content'], id, ))
        rows_affected = db_cursor.rowcount
    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True

def get_posts_by_category(category_id):
    with sqlite3.connect("./mammoth_cave.db") as conn:
        conn.row_factory = sqlite3.Row

        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id,
            p.creation_date,
            p.category_id,
            p.subject,
            p.content,
            u.id,
            u.first_name,
            u.last_name,
            u.email,
            u.password,
            c.id,
            c.name
        FROM posts p
        JOIN users u
            ON u.id = p.user_id
        JOIN categories c
            ON c.id = p.category_id
        WHERE p.category_id = ?
        """, ( int(category_id), ))

        posts = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            post = Post(row['id'], row['user_id'], row['creation_date'], row['category_id'], row['subject'], row['content'])
            user = User(row['user_id'], row['first_name'], row['last_name'], row['email'], row['password'])
            category = Category(row['category_id'], row['name'])

            post.user = user.__dict__

            post.category = category.__dict__

            posts.append(post.__dict__)

        return json.dumps(posts)
