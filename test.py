import sqlite3

database = "my.db"
create_table = """CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY, 
    name text NOT NULL, 
    begin_date DATE, 
    end_date DATE
);"""

try:
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()
        cursor.execute(create_table)   
        conn.commit()

except sqlite3.OperationalError as e:
    print(e)