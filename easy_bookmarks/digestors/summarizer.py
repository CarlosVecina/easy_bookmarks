from adalflow import Generator

from easy_bookmarks.digestors.base_digestor import BaseDigestor


class SummaryGenerator(BaseDigestor):
    _task_desc_str: str = """
    You need to provide an structured summary of several paragraph of the bookmarks of the users,
    so he/she can catch up with the latest posts in his/her bookmarks.
    """

    def summarize(self, text: str) -> str:
        generator = Generator(
            model_client=self.model_client,
            model_kwargs=self.model_kwargs,
            prompt_kwargs={"task_desc_str": self._task_desc_str},
            template=self._template,
        )

        return generator(prompt_kwargs={"input_str": text})
