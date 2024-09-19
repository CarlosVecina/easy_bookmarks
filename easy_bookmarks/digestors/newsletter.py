from adalflow import Generator

from easy_bookmarks.digestors.base_digestor import BaseDigestor


class NewsletterGenerator(BaseDigestor):
    _task_desc_str: str = """
    You need to generate a newsletter based on the bookmarks of the user.
    It should be properly structured and formatted.
    The concepts that fall under the same topic or category should be grouped together.
    Each topic or category need to have a proper headline.
    """

    def run(self, text: str) -> str:
        generator = Generator(
            model_client=self.llm_client,
            model_kwargs=self.llm_kwargs,
            prompt_kwargs={"task_desc_str": self._task_desc_str},
            template=self._template,
        )

        return generator(prompt_kwargs={"input_str": text})
