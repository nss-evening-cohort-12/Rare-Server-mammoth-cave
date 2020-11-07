import sqlite3
import json
from models import Comment

def get_comments_by_post_id(post_id):
    with sqlite3.connect("./mammoth_cave.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            c.id,
            c.user_id,
            c.post_id,
            c.creation_date,
            c.subject,
            c.content
            from comments c
            where c.post_id = ?
            ORDER BY creation_date
          """, (int(post_id), ))

        comments = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            comment = Comment(row['id'], row['user_id'], row['post_id'], row['creation_date'], row['subject'], row['content'])
            comments.append(comment.__dict__)
    return json.dumps(comments)


def create_comment(body):
    with sqlite3.connect('./mammoth_cave.db') as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO comments
            (user_id, post_id, creation_date, subject, content)
        VALUES
            (?,?,?,?,?)
        """, (body['user_id'], body['post_id'], body['creation_date'], body['subject'], body['content']))

        id = db_cursor.lastrowid

        body['id'] = id
    return json.dumps(body)

def delete_comment(id):
    with sqlite3.connect("./mammoth_cave.db") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        DELETE FROM comments
        WHERE id = ?
        """, (id, ))
