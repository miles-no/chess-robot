from database.db_init import create_connection

def add_player(name, score):
    conn = create_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO players (username, score) VALUES (%s, %s)", (name, score))
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
        cur.execute("SELECT username, score FROM players ORDER BY score DESC")
        leaderboard = []
        rows = cur.fetchall()
        for row in rows:
            (username, score) = row
            leaderboard.append({"name": username, "score": score})
        cur.close()
        return leaderboard
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == "__main__":
    add_player("First player", 1000)
    add_player("Second player", 2000)
    print(get_leaderboard())