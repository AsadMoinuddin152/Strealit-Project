import pandas as pd
import psycopg2
from pymongo import MongoClient
import mysql.connector
import streamlit as st

def load_postgresql_tables(host, port, user, password, dbname):
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            dbname=dbname
        )
        query = "SELECT table_name FROM information_schema.tables WHERE table_schema='public';"
        return pd.read_sql_query(query, conn)['table_name'].tolist()
    except Exception as e:
        st.error(f"Error connecting to PostgreSQL: {e}")
        return []
    finally:
        if conn:
            conn.close()

def load_postgresql_data(num_rows, table_name, host, port, user, password, dbname):
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            dbname=dbname
        )
        query = f"SELECT * FROM {table_name} LIMIT {num_rows};"
        return pd.read_sql_query(query, conn)
    except Exception as e:
        st.error(f"Error loading data from PostgreSQL: {e}")
        return None
    finally:
        if conn:
            conn.close()

def load_mongodb_collections(mongo_uri, mongo_db):
    try:
        client = MongoClient(mongo_uri)
        db = client[mongo_db]
        return db.list_collection_names()
    except Exception as e:
        st.error(f"Error connecting to MongoDB: {e}")
        return []
    finally:
        client.close()

def load_mongodb_data(num_rows, collection_name, mongo_uri, mongo_db):
    try:
        client = MongoClient(mongo_uri)
        db = client[mongo_db]
        collection = db[collection_name]
        return pd.DataFrame(list(collection.find().limit(num_rows)))
    except Exception as e:
        st.error(f"Error loading data from MongoDB: {e}")
        return None
    finally:
        client.close()

def load_mysql_tables(host, port, user, password, dbname):
    try:
        conn = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=dbname
        )
        query = "SHOW TABLES;"
        return pd.read_sql(query, conn)['Tables_in_' + dbname].tolist()
    except Exception as e:
        st.error(f"Error connecting to MySQL: {e}")
        return []
    finally:
        if conn:
            conn.close()

def load_mysql_data(num_rows, table_name, host, port, user, password, dbname):
    try:
        conn = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=dbname
        )
        query = f"SELECT * FROM {table_name} LIMIT {num_rows};"
        return pd.read_sql(query, conn)
    except Exception as e:
        st.error(f"Error loading data from MySQL: {e}")
        return None
    finally:
        if conn:
            conn.close()