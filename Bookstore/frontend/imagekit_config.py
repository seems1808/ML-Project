
from imagekitio import ImageKit
import streamlit as st


imagekit = ImageKit(
    private_key=st.secrets["IMAGEKIT_PRIVATE_KEY"]
)


def upload_image(file):

    response = imagekit.files.upload(
        file=file.getvalue(),
        file_name=file.name
    )

    return response.url