from utils.img_converter import encode_image
from prompts.prompts import prompt_get_languages, prompt_pic2notes


def create_LLM_call(image_path: str) -> list[dict[str, str]]:
    return [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt_get_languages,
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
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt_pic2notes,
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
