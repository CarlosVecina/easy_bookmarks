import time
import random
from typing import Any

from linkedin_api import Linkedin
from pydantic import BaseModel


class LinkedinIntegration(BaseModel, Linkedin):
    username: str
    password: str
    client: Any | None = None
    logger: Any | None = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Linkedin.__init__(self, *args, **kwargs)

    def get_bookmarked_posts(self, limit: int = -1) -> list[dict]:
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
                """.replace(
                    "\n", ""
                ).replace(
                    "  ", ""
                )
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
        except:
            return results

        return results
