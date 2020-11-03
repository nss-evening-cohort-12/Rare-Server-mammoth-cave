import sqlite3
import json
from models import Post

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
            p.content
        FROM posts p
        """)

        posts = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            post = Post(row['id'], row['user_id'], row['creation_date'], row['category_id'], row['subject'], row['content'])

            posts.append(post.__dict__)

    return json.dumps(posts)

def get_single_post(id):
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
            p.content
        FROM posts p
        WHERE p.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()

        post = Post(data['id'], data['user_id'], data['creation_date'], data['category_id'], data['subject'], data['content'])

        return json.dumps(post.__dict__)

def create_post(new_post):
    with sqlite3.connect('./mammoth_cave.db') as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        INSERT INTO posts
            (user_id, creation_date, category_id, subject, content)
        VALUES 
            (?, ?, ?, ?, ?);
        """, (new_post['user_id'], new_post['creation_date'], new_post['category_id'], new_post['subject'], new_post['content'], ))
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
        """, (new_post['user_id'], new_post['creation_date'],
              new_post['category_id'], new_post['subject'],
              new_post['content'], id, ))
        rows_affected = db_cursor.rowcount
    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True
