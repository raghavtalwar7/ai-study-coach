from psycopg2.pool import SimpleConnectionPool
import streamlit as st

DATABASE_URL = st.secrets["database"]["url"]

POOL = SimpleConnectionPool(
    minconn=1,
    maxconn=5,
    dsn=DATABASE_URL
)

def get_conn():
    return POOL.getconn()

def release_conn(conn):
    POOL.putconn(conn)
