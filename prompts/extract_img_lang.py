from utils.available_languages import AvailableLanguages
from utils.img_converter import encode_image


def prompt_img_lang(image_path: str) -> list[dict[str, str]]:
    return [
        {
            "role": "system",
            "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair.",
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"Please, output the main language used in the text of the photo, just output a value between this options {AvailableLanguages.list_available_languages()}.",
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{encode_image(image_path)}"
                    },
                },
            ],
        },
    ][
        {
            "role": "system",
            "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair.",
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"Please, output the main language used in the text of the photo, just output a value between this options {AvailableLanguages.list_available_languages()}.",
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{encode_image(image_path)}"
                    },
                },
            ],
        },
    ]
