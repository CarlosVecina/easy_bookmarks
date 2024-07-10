from utils.img_converter import encode_image
from prompts.prompts import prompt_get_languages, prompt_pic2notes


def create_get_lang_call(image_path: str) -> list[dict[str, str]]:
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
    ]


def create_pic2notes(
    image_path: str, extract_text_ocr: list[str]
) -> list[dict[str, str]]:
    composed_prompt = f"""{prompt_pic2notes}. Here there is the text extracted by an OCR tool, 
    in case you find it useful for the task: {extract_text_ocr}."""

    return [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": composed_prompt,
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
