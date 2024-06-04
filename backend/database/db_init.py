from configparser import ConfigParser
import psycopg2

table_players = (
    """
    CREATE TABLE players (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) NOT NULL,
        score INTEGER,
        date TEXT,
        level INTEGER
    )
    """
)

import os

def config():
    db = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'database': os.getenv('DB_NAME','databasename'),
        'user': os.getenv('DB_USER','username'),
        'password': os.getenv('DB_PASSWORD','password')
    }
    for key in db:
        if db[key] is None:
            raise ValueError(f"Environment variable {key} not set")
    return db

def create_connection():
    params = config()
    return psycopg2.connect(**params)

def create_table(table):
     # Connect to the PostgreSQL server
    conn = create_connection()
    cur = conn.cursor()
    try:
        # Create table, close communication with the PostgreSQL database server
        # Commit the changes
        cur.execute(table)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()