import psycopg2

__DBNAME = "meteo_uz"
__USER = "postgres"
__PASSWORD = "p4stgr2s"

cconn = psycopg2.connect(
    host="localhost",
    database=__DBNAME,
    user=__USER,
    password=__PASSWORD)

cconn.autocommit = True

cursor = cconn.cursor()

def create_table(cursor, schema, table_name, column_names, column_types):
    cursor.execute("""CREATE TABLE %s.%s"""%(schema, table_name))
    pass

def drop_table(cursor, schema, table):
    cursor.execute("""DROP TABLE %s.%s""", (schema, table))
    cconn.close()

def insert_into(cursor, schema, table, dict):
    columns = tuple(dict.keys())
    values = tuple(dict.values())
    cursor.execute("""INSERT INTO %s.%s %s VALUES %s"""%(schema, table, columns, values))
    cconn.close()