from models.user import User
import json
import sqlite3

def login_check(creds):
    with sqlite3.connect("./mammoth_cave.db") as conn:
        db_cursor = conn.cursor()
    
        db_cursor.execute("""
        select 
        u.id,
        u.first_name fname,
        u.last_name lname,
        u.email,
        u.password
        from users u
        where u.email=? AND u.password = ?
        """, (creds['username'], creds['password'], ))

        dataset = db_cursor.fetchone()

        if dataset:
            return json.dumps({"valid": True, "token": creds['username']})
        else:
            return json.dumps({})


def add_user(creds):
    with sqlite3.connect("./mammoth_cave.db") as conn:
        db_cursor = conn.cursor()
    
        db_cursor.execute("""
        select 
        u.id,
        u.first_name fname,
        u.last_name lname,
        u.email,
        u.password
        from users u
        where u.email=?
        """, (creds['email'], ))

        dataset = db_cursor.fetchone()

        if dataset:
            return json.dumps({})
        else:
            db_cursor.execute("""
            INSERT INTO users
                ( id, first_name, last_name, email, password, activated )
            VALUES
                ( null, ?, ?, ?, ?, 1);
            """, (creds['first_name'], creds['last_name'], creds['username'], creds['password'], ))

            return json.dumps({"valid": True, "token": creds['username']})
