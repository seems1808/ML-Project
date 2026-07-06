import pandas as pd
import psycopg2

# Read CSV
df = pd.read_csv("data/books.csv")

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="bookstore",
    user="postgres",
    password="admin@123",
    port="5432"
)

cur = conn.cursor()

for _, row in df.iterrows():
    cur.execute("""
        INSERT INTO books
        (id, title, author, category, price, rating, image, description)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (id)
        DO UPDATE SET
            title = EXCLUDED.title,
            author = EXCLUDED.author,
            category = EXCLUDED.category,
            price = EXCLUDED.price,
            rating = EXCLUDED.rating,
            image = EXCLUDED.image,
            description = EXCLUDED.description;
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

print("✅ Books synchronized successfully!")