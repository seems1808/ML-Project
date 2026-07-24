import joblib
from pathlib import Path


BASE_DIR=Path(__file__).parent.parent

MODEL=BASE_DIR/"models"



model=joblib.load(

        MODEL/"book_model.pkl"

        )


category_encoder=joblib.load(

            MODEL/"category.pkl"

            )


author_encoder=joblib.load(

            MODEL/"author.pkl"

            )


title_encoder=joblib.load(

            MODEL/"title.pkl"

            )


#---------------------------------

def predict_book(

        category,
        author,
        price,
        rating

        ):


    try:

        category=category_encoder.transform(
                        [category]
                    )[0]


        author=author_encoder.transform(
                        [author]
                    )[0]


        prediction=model.predict(

                    [[

                    category,
                    author,
                    price,
                    rating

                    ]]

                )


        result=title_encoder.inverse_transform(
                    prediction
                )[0]


        return result


    except:

        return "No Recommendation Found"
    
