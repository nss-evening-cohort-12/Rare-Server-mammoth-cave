from models.user import User
import json
import sqlite3

def login_check(creds):
     print(creds)
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
            print(dataset)
            return json.dumps({"valid": True, "token": "genericToken"})
        else:
            return json.dumps({})
