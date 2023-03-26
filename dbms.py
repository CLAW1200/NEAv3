import sqlite3
con = sqlite3.connect("main.db")
cur = con.cursor()

def create_table():
    cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, highScore INTEGER)")
    con.commit()
    con.close()

def insert(username, highScore):
    cur.execute("INSERT INTO users VALUES (NULL, ?, ?)", (username, highScore))
    con.commit()                          
    con.close()

def view():
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    con.close()                                                                                      
    return rows                                                

def delete(id):
    cur.execute("DELETE FROM users WHERE id=?", (id,))
    con.commit()
    con.close()

def update(id, username, highScore):
    cur.execute("UPDATE users SET username=?, highScore=? WHERE id=?", (username, highScore, id))
    con.commit()
    con.close()

def search(username="", highScore=""):
    cur.execute("SELECT * FROM users WHERE username=? OR highScore=?", (username, highScore))
    rows = cur.fetchall()
    con.close()
    return rows

create_table()
insert("John", 100)
print(view())