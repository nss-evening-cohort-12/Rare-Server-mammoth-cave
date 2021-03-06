from models.user import User
import json
import sqlite3

def login_check(creds):
    with sqlite3.connect("./mammoth_cave.db") as conn:
        conn.row_factory = sqlite3.Row
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
            retval = json.dumps({"valid": True, "token": dataset['id']})
            return retval
            # return json.dumps({"valid": True, "token": dataset['id']})
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
                ( id, first_name, last_name, email, password, activated, bio )
            VALUES
                ( null, ?, ?, ?, ?, 1, ?);
            """, (creds['first_name'], creds['last_name'], creds['username'], creds['password'], creds['bio'] ))

            id = db_cursor.lastrowid


            return json.dumps({"valid": True, "token": id})


def get_all_users():
    with sqlite3.connect("./mammoth_cave.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
    
        db_cursor.execute("""
        select 
            u.id,
            u.first_name fname,
            u.last_name lname,
            u.email,
            u.password,
            u.activated,
            u.bio
        from users u
        """)

        users = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            user = User(row['id'], row['fname'], row['lname'], row['email'], row['password'],row['bio'])

            users.append(user.__dict__)
        
        return json.dumps(users)


def get_single_user(id):
    with sqlite3.connect("./mammoth_cave.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
    
        db_cursor.execute("""
        select 
            u.id,
            u.first_name fname,
            u.last_name lname,
            u.email,
            u.password,
            u.activated,
            u.bio
        from users u
        where u.id = ?
        """, (int(id), ))


        row = db_cursor.fetchone()

        user = User(row['id'], row['fname'], row['lname'], row['email'], row['password'], row['bio'])

        
        return json.dumps(user.__dict__)
