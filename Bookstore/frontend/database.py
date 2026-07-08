import psycopg2

def get_connection():
    conn = psycopg2.connect(
        host="ep-small-wildflower-at3s58wt.c-9.us-east-1.aws.neon.tech",
        database="neondb",
        user="neondb_owner",
        password="npg_yVXWeOH3gnJ1",
        port="5432",
        sslmode="require"
    )
    return conn