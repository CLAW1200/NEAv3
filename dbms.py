import sqlite3
con = sqlite3.connect("main.db")
cur = con.cursor()

def create_table():
    cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, highScore INTEGER)")
    con.commit()
    con.close()

"""A function to add a new user to the database"""
def add_user(username, highScore):
    con = sqlite3.connect("main.db")
    cur = con.cursor()
    cur.execute("INSERT INTO users VALUES (NULL, ?, ?)", (username, highScore))
    con.commit()
    con.close()

"""A function to get all the users from the database"""
def get_users():
    con = sqlite3.connect("main.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    con.close()
    return users

"""A function to get a user from the database"""
def get_user(username):
    con = sqlite3.connect("main.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cur.fetchone()
    con.close()
    return user
    

"""A function to update a user's high score"""
def update_high_score(username, highScore):
    con = sqlite3.connect("main.db")
    cur = con.cursor()
    cur.execute("UPDATE users SET highScore = ? WHERE username = ?", (highScore, username))
    con.commit()
    con.close()

"""A function to delete a user from the database"""
def delete_user(username):
    con = sqlite3.connect("main.db")
    cur = con.cursor()
    cur.execute("DELETE FROM users WHERE username = ?", (username,))
    con.commit()
    con.close()

"""A function to delete all the users from the database"""
def delete_all_users():
    con = sqlite3.connect("main.db")
    cur = con.cursor()
    cur.execute("DELETE FROM users")
    con.commit()
    con.close()


if __name__ == "__main__":
    create_table()
    add_user("test", 0)
    add_user("test2", 0)
    add_user("test3", 0)
    print(get_users())
    print(get_user("test"))
    update_high_score("test", 100)
    print(get_user("test"))
    delete_user("test")
    print(get_users())
    delete_all_users()
    print(get_users())