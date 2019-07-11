import os
import requests


def check_image_similarity(image1, image2):
    r = requests.post(
        "https://api.deepai.org/api/image-similarity",
        files={
            'image1': image1,
            'image2': image2,
        },
        headers={'api-key': os.getenv("DEEP_AI_API_KEY")}
    )

    print(r.json())

    return r.json()['output']['distance']
