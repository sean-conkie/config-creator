from sqlite3 import connect, Error, version


def create_connection(db_file):
    conn = None
    try:
        conn = connect(db_file)
        print(version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    create_connection(r"./config_creator/db.sqlite3")
