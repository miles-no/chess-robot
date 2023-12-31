from database.db_init import create_connection
from datetime import datetime

def add_player(name, score, date, level):
    conn = create_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO players (username, score, date, level) VALUES (%s, %s, %s, %s)", (name, score, date, level))
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def get_leaderboard():
    conn = create_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT username, score, date, level FROM players ORDER BY score DESC")
        leaderboard = []
        rows = cur.fetchall()
        for row in rows:
            (username, score, date, level) = row
            leaderboard.append({"name": username, "score": score, "date": date, "level": level})
        cur.close()
        return leaderboard
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()