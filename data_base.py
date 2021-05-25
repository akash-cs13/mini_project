import sqlite3


conn = sqlite3.connect('data.db')
cur = conn.cursor()

initalise = '''CREATE TABLE IF NOT EXISTS known(
                name text,
                known_img txt,
                recent_img txt
)'''

cur.execute(initalise)

cur.execute("SELECT * FROM known")
print(cur.fetchall())


conn.commit()


for command in open('initial.txt','r'):
    cur.execute(command)
    conn.commit()



conn.close()
