from configparser import ConfigParser
import psycopg2

table_players = (
    """
    CREATE TABLE players (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) NOT NULL,
        score INTEGER
    )
    """
)

def config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        parms = parser.items(section)
        for parm in parms:
            db[parm[0]] = parm[1]
    else:
        raise Exception ('Section {0} not found in the {1} file'.format(section, filename))
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

if __name__ == '__main__':
    create_table(table_players)