import datetime
import random
import re
import time
from typing import Any
import logging

import polars as pl
import polars.selectors as cs

from linkedin_api import Linkedin
from pydantic import BaseModel

from easy_bookmarks.stores.utils import generate_uuid


logger = logging.getLogger(__name__)


class LinkedinIntegration(BaseModel, Linkedin):
    username: str
    password: str
    client: Any | None = None
    logger: Any | None = None

    source: str = "linkedin"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Linkedin.__init__(self, *args, **kwargs)

    def _get_bookmarked_posts(self, limit: int = -1) -> list[dict]:
        results = []
        pagination_token = None
        start = None
        count = 10

        try:
            while len(results) < limit or limit == -1:
                if limit > -1 and limit - len(results) < count:
                    count = limit - len(results)

                query = f"""
                /graphql
                ?variables=(
                    {f"{start}," if start else ""}
                    count:{count},
                    {f"{pagination_token}," if pagination_token else ""}
                    query:(
                        flagshipSearchIntent:SEARCH_MY_ITEMS_SAVED_POSTS,
                        queryParameters:List((key:savedPostType,value:List(ALL)))
                    )
                )
                &queryId=voyagerSearchDashClusters.a2b606e8c1f58b3cf72fb5d54a2a57e7
                """.replace("\n", "").replace("  ", "")
                print(query)

                res = self._fetch(query)

                post_list = res.json()["data"]["searchDashClustersByAll"]["elements"][
                    0
                ]["items"]

                if len(post_list) == 0:
                    break

                for post in post_list:
                    extracted_posts = {
                        "author": post["item"]["entityResult"]["title"]["text"],
                        "author_catchline": post["item"]["entityResult"][
                            "primarySubtitle"
                        ]["text"],
                        "author_member_id": post["item"]["entityResult"][
                            "actorTrackingUrn"
                        ].split(":")[-1],
                        "post_summary": post["item"]["entityResult"]["summary"]["text"],
                        "post_url": post["item"]["entityResult"]["navigationUrl"],
                        "post_activity_id": post["item"]["entityResult"][
                            "trackingUrn"
                        ].split(":")[-1],
                        "post_date_repost_info": post["item"]["entityResult"][
                            "secondarySubtitle"
                        ]["text"],
                    }

                    results.append(extracted_posts)

                pagination_token = f'paginationToken:{res.json()["data"]["searchDashClustersByAll"]["metadata"]["paginationToken"]}'
                start = f"start:{len(results)}"

                print(f"Total {len(results)} values retrieved")

                time.sleep(random.randint(1, 3))
        except Exception as e:
            logger.warning(f"Error fetching LinkedIn posts: {e}")
            return results

        return results

    def get_bookmarked_df(self, limit: int = -1) -> pl.DataFrame:
        posts = self._get_bookmarked_posts(limit)

        df = pl.from_records(
            posts, orient="row"
        )  # , schema=self.get_bookmarked_posts(limit)[0].keys())

        # Parse date
        df = df.with_columns(
            pl.col("post_date_repost_info")
            .str.split(" • ")
            .map_elements(self._parse_linkedin_date)
            .alias("parsed_date")
        ).drop(["post_date_repost_info"])

        # Add source and id
        df = df.with_columns(
            pl.lit(self.source).alias("source"),
        ).with_columns(
            (pl.col("source") + pl.col("post_url"))
            .map_elements(generate_uuid)
            .cast(pl.Utf8)
            .alias("uuid")
        )

        return df.select(["uuid", "source"], cs.all())

    @staticmethod
    def _parse_linkedin_date(parts):
        basic_map_date = {
            "m": "minutes",
            "h": "hours",
            "d": "days",
            "w": "weeks",
        }
        complex_map_date = {
            "mo": ("weeks", 4),
            "yr": ("weeks", 52),
        }

        list_match = [
            match for part in parts if (match := re.match(r"(\d+)\s*(\w+)", part))
        ]

        if len(list_match) != 1:
            return None

        value, unit = list_match[0].groups()
        unit = unit.rstrip("s")
        if unit in basic_map_date.keys():
            delta = datetime.timedelta(
                **{basic_map_date[unit]: int(value)}
            )  # return pd.Timestamp.now() - delta
            return datetime.datetime.now().date() - delta
        else:
            complex_unit, multiplier = complex_map_date[unit]
            delta = datetime.timedelta(**{complex_unit: int(value) * multiplier})
            return datetime.datetime.now().date() - delta
