import ast
import logging
import os
from typing import Iterator

from adalflow import Generator
from elevenlabs import VoiceSettings, save
from elevenlabs.client import ElevenLabs
from pydantic import ConfigDict
from pydantic_settings import BaseSettings
from pydub import AudioSegment

from easy_bookmarks.digestors.base_digestor import BaseDigestor

logger = logging.getLogger(__name__)


class ElevenLabsConfig(BaseSettings):
    model_config = ConfigDict(env_prefix="ELEVENLABS_")
    api_key: str


class PodcastAgent(BaseDigestor):
    # for now super coupled to elevenlabs
    # some copypasta from https://github.com/SaschaHeyer/gen-ai-livestream/blob/main/podcast-automation/generate.py
    _task_desc_str: str = """you are an experienced podcast host...
    - based on the latest news and articles you can create an engaging conversation between two people.
    - the conversation should by in English.
    - make the conversation at least 10000 characters long with a lot of emotion.
    - in the response for me to identify use Carlos and Ana.
    - Ana is writing the articles and Marina is the second speaker that is asking all the good questions.
    - The podcast is called Easy Bookmarks - Easy Content Consumption.
    - Short sentences that can be easily used with speech synthesis.
    - excitement during the conversation.
    - do not mention last names.
    - Carlos and Ana are doing this podcast together. Avoid sentences like: "Thanks for having me, Marina!"
    - Include filler words like äh or repeat words to make the conversation more natural.
    """
    speaker_voice_map: dict[str, str] = {
        "Carlos": "L0Dsvb3SLTyegXwtm47J",
        "Ana": "pMsXgVXv3BLzUgSXRplE",
    }
    elevenlabs_config: ElevenLabsConfig = ElevenLabsConfig()

    _tts_client: ElevenLabs | None = None

    def _generate_podcast_script(self, text: str) -> str:
        output_format_str = r"""Your output should be formatted as a list of tuples. Example:
        [
            ("Carlos", "Hello, how are you today?"),
            ("Ana", "I'm doing great, thank you! How about you?"),
            ("Carlos", "I'm doing well, thanks! And you?"),
            ("Ana", "I'm doing great, thank you! How about you?"),
        ]
        """

        generator = Generator(
            model_client=self.llm_client,
            model_kwargs=self.llm_kwargs,
            template=self._template,
            prompt_kwargs={
                "task_desc_str": self._task_desc_str,
                "output_format_str": output_format_str,
            },
            # output_processors=ListParser(), TODO: Move to this output processor
        )

        text = generator(prompt_kwargs={"input_str": text}).data
        return ast.literal_eval(text)

    def _start_elevenlabs_client(self):
        if not self._tts_client:
            self._tts_client = ElevenLabs(**self.elevenlabs_config.model_dump())

    def _get_elevenlabs_audio(self, text: str, speaker: str) -> Iterator[bytes]:
        self._start_elevenlabs_client()

        voice = self.speaker_voice_map[speaker]

        response = self._tts_client.generate(
            voice=voice,
            optimize_streaming_latency="0",
            output_format="mp3_22050_32",
            text=text,
            voice_settings=VoiceSettings(
                stability=0.1,
                similarity_boost=0.3,
                style=0.2,
            ),
        )
        return response

    def _save_audio(
        self,
        response: Iterator[bytes],
        export_name: str,
        export_path: str = "data/audio",
    ):
        save(response, f"{export_path}/{export_name}.mp3")

        return response

    def merge_audios(audio_folder: str, output_file: str = "/combined.mp3"):
        combined = AudioSegment.empty()
        audio_files = sorted(
            [
                f
                for f in os.listdir(audio_folder)
                if f.endswith(".mp3") or f.endswith(".wav")
            ],
            key=lambda x: int(x.split("_")[1].split(".")[0]),
        )
        for filename in audio_files:
            audio_path = os.path.join(audio_folder, filename)
            logger.info(f"Processing: {audio_path}")
            audio = AudioSegment.from_file(audio_path)
            combined += audio
        combined.export(audio_folder + output_file, format="mp3")
        logger.info(f"Merged audio saved as {output_file}")

    def run(self, text: str):
        logger.info("Generating podcast script")
        transcript = self._generate_podcast_script(text)
        logger.info("Podcast script generated!")
        with open("data/transcript.txt", "w") as f:
            f.write(str(transcript))

        for i, (speaker, text) in enumerate(transcript):
            audio = self._get_elevenlabs_audio(text, speaker)
            self._save_audio(audio, f"{speaker}_{i}.mp3")
            logger.info(f"Podcast audio {i} generated!")
