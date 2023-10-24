from db_connection_solution import *

if __name__ == '__main__':
    conn = connectDataBase()
    cur = conn.cursor()

    createTables(cur, conn)