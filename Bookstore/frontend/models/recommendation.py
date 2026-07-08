import pandas as pd
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------- Paths ----------------
BASE_DIR = Path(__file__).parent.parent
DATA = BASE_DIR / "data"


def recommend_books(book_title):

    # Load latest dataset every time
    df = pd.read_csv(DATA / "books.csv")

    # Find selected book
    selected = df[df["title"] == book_title]

    if selected.empty:
        return []

    # Get selected category
    category = selected.iloc[0]["category"]

    # Keep only books from the same category
    same_category = df[df["category"] == category].reset_index(drop=True)

    # If only one book exists
    if len(same_category) <= 1:
        return []

    # Use title + author + description as content
    same_category["content"] = (
        same_category["title"].fillna("") + " " +
        same_category["author"].fillna("") + " " +
        same_category["description"].fillna("")
    )

    # TF-IDF Vectorization
    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(same_category["content"])

    # Cosine Similarity
    similarity = cosine_similarity(tfidf_matrix)

    # Selected book index
    index = same_category[
        same_category["title"] == book_title
    ].index[0]

    # Similarity scores
    scores = list(enumerate(similarity[index]))

    # Sort by similarity
    scores = sorted(
        scores,
        key=lambda x: x[1],
        reverse=True
    )

    # Remove selected book itself
    scores = scores[1:4]

    recommendations = []

    for i, score in scores:
        recommendations.append(
            same_category.iloc[i].to_dict()
        )

    return recommendations