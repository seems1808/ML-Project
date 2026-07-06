import pandas as pd
import psycopg2

# Read CSV
df = pd.read_csv("frontend/data/books.csv")

# Connect to Neon
def get_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="bookstore",      # Replace with your local database name
        user="postgres",           # Your PostgreSQL username
        password="admin@123",  # Your PostgreSQL password
        port="5432"
    )
    return conn

cur = conn.cursor()

for _, row in df.iterrows():
    cur.execute("""
        INSERT INTO books
        (id, title, author, category, price, rating, image, description)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (id) DO NOTHING;
    """, (
        int(row["id"]),
        row["title"],
        row["author"],
        row["category"],
        int(row["price"]),
        int(row["rating"]),
        row["image"],
        row["description"]
    ))

conn.commit()
cur.close()
conn.close()

print("✅ Books imported successfully!")