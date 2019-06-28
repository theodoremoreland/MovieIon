import pandas as pd
import psycopg2
from psycopg2 import Error
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from config import user, password, host, port, database

try:
    connection = psycopg2.connect(user=user,
                                  password=password,
                                  host=host,
                                  port=port,
                                  database=database)
    cursor = connection.cursor()
    # Print PostgreSQL Connection properties
    print(connection.get_dsn_parameters(), "\n")
    # Print PostgreSQL version
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("You are connected to - ", record, "\n")

    engine = create_engine(
        f"postgresql://{user}:{password}@{host}:{port}/{database}")
    con = engine.connect()
    movie_df = pd.read_csv()
    movie_df.set_index("movie_id", inplace=True)
    print(movie_df.head())
    movie_df.to_sql('movie_list', engine, if_exists="append")
except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    # closing database connection.
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")

# import pandas as pd
# import csv
# from io import StringIO
# from sqlalchemy import create_engine


# def psql_insert_copy(table, conn, keys, data_iter):
#     # gets a DBAPI connection that can provide a cursor
#     dbapi_conn = conn.connection
#     with dbapi_conn.cursor() as cur:
#         s_buf = StringIO()
#         writer = csv.writer(s_buf)
#         writer.writerows(data_iter)
#         s_buf.seek(0)

#         columns = ', '.join('"{}"'.format(k) for k in keys)
#         if table.schema:
#             table_name = '{}.{}'.format(table.schema, table.name)
#         else:
#             table_name = table.name

#         sql = 'COPY {} ({}) FROM STDIN WITH CSV'.format(
#             table_name, columns)
#         cur.copy_expert(sql=sql, file=s_buf)


# link_df = pd.read_csv()


# link_df.to_sql('link_list', engine, method=psql_insert_copy)

