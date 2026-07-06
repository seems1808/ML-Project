import psycopg2
import streamlit as st
def get_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="bookstore",      # Replace with your local database name
        user="postgres",           # Your PostgreSQL username
        password="admin@123",  # Your PostgreSQL password
        port="5432"
    )
    return conn
  
