import pandas as pd
import psycopg2


# -----------------------------
# Read CSV File
# -----------------------------

df = pd.read_csv("data/books.csv")


# -----------------------------
# Database Connection
# -----------------------------

def get_connection():

    conn = psycopg2.connect(
        host="localhost",
        database="bookstore",
        user="postgres",
        password="admin@123",
        port="5432"
    )

    return conn


# -----------------------------
# Connect to Database
# -----------------------------

conn = get_connection()
cur = conn.cursor()


# -----------------------------
# Insert Books into Database
# -----------------------------

for _, row in df.iterrows():

    cur.execute(
        """
        INSERT INTO books
        (
            id,
            title,
            author,
            category,
            price,
            rating,
            image,
            description
        )

        VALUES
        (
            %s,%s,%s,%s,%s,%s,%s,%s
        )

        ON CONFLICT (id) DO NOTHING;
        """,

        (
            int(row["id"]),
            row["title"],
            row["author"],
            row["category"],
            float(row["price"]),
            float(row["rating"]),
            row["image"],
            row["description"]
        )

    )


# -----------------------------
# Save Changes
# -----------------------------

conn.commit()


# -----------------------------
# Close Connection
# -----------------------------

cur.close()
conn.close()


print("Books imported successfully!")