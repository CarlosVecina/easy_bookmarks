import os
import easyocr
from openai import OpenAI
from dotenv import load_dotenv

from pic2bookmark.prompts.llm_calls import create_get_lang_call, create_pic2notes
from pic2bookmark.utils.available_languages import AvailableLanguages

load_dotenv()

INPUT_PATH = './images'
OUTPUT_PATH = './outputs'


def get_photo_main_language(llm_client: OpenAI, image_path: str) -> AvailableLanguages:
    completion = llm_client.chat.completions.create(
        model="gpt-4o",
        messages=create_get_lang_call(image_path),
    )

    return [AvailableLanguages(completion.choices[0].message.content).value]


def extract_text_ocr(image_path: str, lang: list[AvailableLanguages]) -> list[str]:
    reader = easyocr.Reader(lang)
    return reader.readtext(image_path, detail=0)

def extract_content_openai(llm_client: OpenAI, image_path: str, extract_text_ocr: list[str]) -> str:
    completion = llm_client.chat.completions.create(
        model="gpt-4o",
        messages=create_pic2notes(image_path, extract_text_ocr),
    )
    return completion.choices[0].message.content

def main(llm_client: OpenAI, image_path: str) -> str:
    pic_main_lang = get_photo_main_language(llm_client=llm_client, image_path=image_path)
    output_ocr = extract_text_ocr(image_path=image_path, lang=pic_main_lang)
    final_output = extract_content_openai(llm_client=llm_client, image_path=image_path, extract_text_ocr=output_ocr)
    return final_output


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Extract text from images and create notes using OpenAI's GPT-4.")

    parser.add_argument(
        "--input",
        type=str,
        default=None,
        help="Path to the folder or to the image to process.",
        required=False,
    )

    args = parser.parse_args()

    if args.input is None:
        raise ValueError("Please provide input file or input path.")
    
    if os.path.isfile(args.input):
        list_input_paths: list[str] = [args.input]
    else:
        list_input_paths: list[str] = [f"{args.input}/{img}" for img in os.listdir(args.input)]
    

    llm_client = OpenAI()

    for image_path in list_input_paths:
        print(f"Processing image: {image_path}")

        final_output = main(llm_client, image_path)

        with open(f"{OUTPUT_PATH}/{image_path.split('.')[0]}.txt", "w") as text_file:
            text_file.write(final_output)

        print("Text extracted and saved in output folder!!")
