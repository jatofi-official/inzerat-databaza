import sqlite3

with sqlite3.connect('database.db') as connection:

    # Create a cursor object
    cursor = connection.cursor()

    # Create Users table
    create_users = '''
    CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        username TEXT NOT NULL,
        age INTEGER,
        email TEXT,
        phone INTEGER
    );
    '''
    create_adverts = '''
    CREATE TABLE IF NOT EXISTS Adverts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        date_created DATE,
        user TEXT,
        price INTEGER,
        section TEXT,
        theme TEXT
    );
    '''

    cursor.execute(create_users)
    cursor.execute(create_adverts)

    # Commit the changes
    connection.commit()