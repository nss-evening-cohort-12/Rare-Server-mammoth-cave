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
            p.user_name,
            p.creation_date,
            p.category_id,
            p.subject,
            p.content
        FROM posts p
        """)

        posts = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            post = Post(row['id'], row['user_name'], row['creation_date'], row['category_id'], row['subject'], row['content'])

            posts.append(post.__dict__)

    return json.dumps(posts)
