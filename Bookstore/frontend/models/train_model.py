import pandas as pd
import joblib

from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder


#--------------------------

BASE_DIR=Path(__file__).parent.parent

DATA=BASE_DIR/"data"

MODEL=BASE_DIR/"models"

#--------------------------

df=pd.read_csv(DATA/"books.csv")


#--------------------------

category_encoder=LabelEncoder()

author_encoder=LabelEncoder()

title_encoder=LabelEncoder()


#--------------------------

df["category"]=category_encoder.fit_transform(
                df["category"]
            )


df["author"]=author_encoder.fit_transform(
                df["author"]
            )


y=title_encoder.fit_transform(

        df["title"]

        )


X=df[
        [
            "category",
            "author",
            "price",
            "rating"
        ]
    ]


#--------------------------

model=RandomForestClassifier(

        n_estimators=100,
        random_state=42

        )


model.fit(X,y)


#--------------------------

joblib.dump(

        model,
        MODEL/"book_model.pkl"

        )


joblib.dump(

        category_encoder,
        MODEL/"category.pkl"

        )


joblib.dump(

        author_encoder,
        MODEL/"author.pkl"

        )


joblib.dump(

        title_encoder,
        MODEL/"title.pkl"

        )


print("\nModel Trained Successfully.")
