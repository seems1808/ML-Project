import pandas as pd
import joblib

from pathlib import Path
from database import get_connection


# --------------------------------------------------
# PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).parent.parent

MODEL = BASE_DIR / "models"


# --------------------------------------------------
# LOAD THE MODEL
# --------------------------------------------------

model = joblib.load(
    MODEL / "book_model.pkl"
)

category_encoder = joblib.load(
    MODEL / "category.pkl"
)

author_encoder = joblib.load(
    MODEL / "author.pkl"
)

title_encoder = joblib.load(
    MODEL / "title.pkl"
)


# --------------------------------------------------
# LOAD BOOKS FROM DATABASE
# --------------------------------------------------

def load_books():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            title,
            author,
            category,
            price,
            rating,
            image,
            description
        FROM books
        """
    )

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    books = []

    for row in rows:

        books.append({

            "id": row[0],
            "title": row[1],
            "author": row[2],
            "category": row[3],
            "price": row[4],
            "rating": row[5],
            "image": row[6],
            "description": row[7]

        })

    return pd.DataFrame(books)


# --------------------------------------------------
# RECOMMEND BOOKS
# --------------------------------------------------

def recommend_books(book_title):

    # Load latest books from Neon Database
    df = load_books()

    # Selected book
    selected_book = df[
        df["title"] == book_title
    ]

    # Book not found
    if selected_book.empty:

        return []


    category = selected_book.iloc[0]["category"]
    author = selected_book.iloc[0]["author"]
    price = selected_book.iloc[0]["price"]
    rating = selected_book.iloc[0]["rating"]


    # --------------------------------------------------
    # HANDLE NEW AUTHORS / CATEGORIES
    # --------------------------------------------------

    try:

        category = category_encoder.transform(
            [category]
        )[0]

    except:

        return []


    try:

        author = author_encoder.transform(
            [author]
        )[0]

    except:

        return []


    # --------------------------------------------------
    # PREPARE INPUT
    # --------------------------------------------------

    input_data = [[

        category,
        author,
        price,
        rating

    ]]


    # --------------------------------------------------
    # GET PROBABILITIES
    # --------------------------------------------------

    probabilities = model.predict_proba(
        input_data
    )[0]


    # Highest probability first
    indexes = probabilities.argsort()[::-1]


    recommendations = []


    # --------------------------------------------------
    # TOP 3 RECOMMENDATIONS
    # --------------------------------------------------

    for index in indexes:

        predicted_title = title_encoder.inverse_transform(
            [index]
        )[0]


        # Skip selected book
        if predicted_title == book_title:
            continue


        book = df[
            df["title"] == predicted_title
        ]


        if not book.empty:

            recommendations.append(

                book.iloc[0].to_dict()

            )


        # Stop at Top-3 books
        if len(recommendations) == 3:
            break


    return recommendations