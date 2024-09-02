from pydantic import BaseModel
import requests
import json


class NotionUploader(BaseModel):
    token: str

    def create_notion_page(self, database_id, title, content_summary, content):
        def construct_headers():
            return {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
                "Notion-Version": "2022-06-28",
            }

        def construct_body():
            return {
                "parent": {"database_id": database_id},
                "properties": {"title": [{"text": {"content": title}}]},
                "children": [
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {"content": content_summary},
                                }
                            ]
                        },
                    },
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [
                                {"type": "text", "text": {"content": content}}
                            ]
                        },
                    },
                ],
            }

        def make_request(data, headers):
            url = "https://api.notion.com/v1/pages"
            response = requests.post(
                url, headers=headers, data=json.dumps(data)
            )
            return response

        def handle_response(response):
            if response.status_code == 200:
                print("Page created successfully!")
            else:
                print(
                    f"Failed to create page: {response.status_code} - {response.text}"
                )

        try:
            headers = construct_headers()
            data = construct_body()
            response = make_request(data, headers)
            handle_response(response)
            return response
        except ValueError as e:
            print(f"Input validation error: {e}")
        except requests.exceptions.RequestException as e:
            print(f"HTTP request error: {e}")
