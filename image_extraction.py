from enum import Enum
import os
import easyocr
from openai import OpenAI

INPUT_PATH = './images'
OUTPUT_PATH = './outputs'


class AvailableLanguages(Enum):
    ENGLISH = 'en'
    FRENCH = 'fr'
    SPANISH = 'es'
    GERMAN = 'de'


def get_photo_main_language(image_path: str) -> AvailableLanguages:
    #TODO: Mock down
    return [AvailableLanguages.ENGLISH.value]

def extract_text_ocr(image_path: str, lang: list[AvailableLanguages]) -> list[str]:
    reader = easyocr.Reader(lang)
    return reader.readtext(image_path, detail=0)

def extract_content_openai(image_path: str, extract_text_ocr: list[str]) -> str:
    #TODO: Mock down
    return "Esto es lo que he podido hacer: " + ' '.join(extract_text_ocr)


if __name__ == '__main__':
    image_path = f"{INPUT_PATH}/shuttle_bus.jpeg"

    OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    pic_main_lang = get_photo_main_language(image_path=image_path)
    output_ocr = extract_text_ocr(image_path=image_path, lang=pic_main_lang)
    final_output = extract_content_openai(image_path=image_path, extract_text_ocr=output_ocr)

    with open(f"{OUTPUT_PATH}/shuttle_bus.txt", "w") as text_file:
        text_file.write(final_output)

    print("Text extracted and saved in output folder")
