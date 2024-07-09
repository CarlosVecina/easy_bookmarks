import os
import easyocr
from openai import OpenAI
from dotenv import load_dotenv

from prompts.extract_img_lang import prompt_img_lang
from utils.available_languages import AvailableLanguages

load_dotenv()

INPUT_PATH = './images'
OUTPUT_PATH = './outputs'


def get_photo_main_language(llm_client: OpenAI, image_path: str) -> AvailableLanguages:
    completion = llm_client.chat.completions.create(
        model="gpt-4o",
        messages=prompt_img_lang(image_path),
    )

    return [AvailableLanguages(completion.choices[0].message.content)]


def extract_text_ocr(image_path: str, lang: list[AvailableLanguages]) -> list[str]:
    reader = easyocr.Reader(lang)
    return reader.readtext(image_path, detail=0)

def extract_content_openai(llm_client: OpenAI, image_path: str, extract_text_ocr: list[str]) -> str:
    # TODO: Insert specific prompts
    #completion = llm_client.chat.completions.create(
    #    model="gpt-4o",
    #    # messages=prompt_img_ocr(image_path),
    #)
    #return completion.choices[0].message.content
    return " ".join(extract_text_ocr)


if __name__ == '__main__':
    image_path = f"{INPUT_PATH}/shuttle_bus.jpeg"

    llm_client = OpenAI()

    pic_main_lang = get_photo_main_language(llm_client=llm_client, image_path=image_path)
    output_ocr = extract_text_ocr(image_path=image_path, lang=pic_main_lang)
    final_output = extract_content_openai(llm_client=llm_client, image_path=image_path, extract_text_ocr=output_ocr)

    with open(f"{OUTPUT_PATH}/shuttle_bus.txt", "w") as text_file:
        text_file.write(final_output)

    print("Text extracted and saved in output folder")
