import os
from pydantic import BaseModel
import requests
import json
from dotenv import load_dotenv


class NotionUploader(BaseModel):
    token: str

    def create_notion_page(self, database_id, title, content):
        def construct_headers():
            return {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
                "Notion-Version": "2022-06-28"
            }

        def construct_body():
            return {
                "parent": { "database_id": database_id },
                "properties": {
                    "title": [
                        {
                            "text": {
                                "content": title
                            }
                        }
                    ]
                },
                "children": 
                    content
                    #{
                       # "object": "block",
                        #"type": "paragraph",
                        #"paragraph": {
                        #    "rich_text": [
                          #      {
                             #       "type": "text",
                                #    "text": {
                                 #       "content": content
                                  #  }
                               # }
                            #]
                        #}
                    #}
                
            }

        def make_request(data, headers):
            url = "https://api.notion.com/v1/pages"
            response = requests.post(url, headers=headers, data=json.dumps(data))
            return response

        def handle_response(response):
            if response.status_code == 200:
                print("Page created successfully!")
            else:
                print(f"Failed to create page: {response.status_code} - {response.text}")

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

if __name__ == "__main__":
    load_dotenv()

    uploader = NotionUploader(token=os.environ["NOTION_TOKEN"])
    uploader.create_notion_page(database_id="69063e81e25b479db72122690a9e2f54", title="Title", content=[
    {
        "object": "block",
        "type": "heading_1",
        "heading_1": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": "Run Gili's Ticketing Service",
                        "link": None
                    }
                }
            ],
            "color": "default",
            "is_toggleable": False
        }
    },
    {
        "object": "block",
        "type": "heading_2",
        "heading_2": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": "Service Information",
                        "link": None
                    }
                }
            ],
            "color": "default",
            "is_toggleable": False
        }
    },
    {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": "Run Gili's Ticketing Service provides shuttle bus services to various destinations from Gili Meno.",
                        "link": None
                    }
                }
            ],
            "color": "default"
        }
    },
    {
        "object": "block",
        "type": "heading_2",
        "heading_2": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": "Contact Information",
                        "link": None
                    }
                }
            ],
            "color": "default",
            "is_toggleable": False
        }
    },
    {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": "+6282146661125",
                        "link": None
                    }
                }
            ],
            "color": "default"
        }
    },
    {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": "+6281907204467",
                        "link": None
                    }
                }
            ],
            "color": "default"
        }
    },
    {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": "Rungilis.Bussnies.goggel.com",
                        "link": None
                    }
                }
            ],
            "color": "default"
        }
    },
    {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": "Runbeachboy92@gmail.com",
                        "link": None
                    }
                }
            ],
            "color": "default"
        }
    },
    {
        "object": "block",
        "type": "heading_2",
        "heading_2": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": "Shuttle Bus Destinations and Prices",
                        "link": None
                    }
                }
            ],
            "color": "default",
            "is_toggleable": False
        }
    },
    {
        "object": "block",
        "type": "table",
        "table": {
            "table_width": 3,
            "has_column_header": True,
            "has_row_header": False,
            "children": [
                {
                    "object": "block",
                    "type": "table_row",
                    "table_row": {
                        "cells": [
                            {
                                "object": "block",
                                "type": "table_cell",
                                "table_cell": {
                                    "rich_text": [
                                        {
                                            "type": "text",
                                            "text": {
                                                "content": "No",
                                                "link": None
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                "object": "block",
                                "type": "table_cell",
                                "table_cell": {
                                    "rich_text": [
                                        {
                                            "type": "text",
                                            "text": {
                                                "content": "Destinations",
                                                "link": None
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                "object": "block",
                                "type": "table_cell",
                                "table_cell": {
                                    "rich_text": [
                                        {
                                            "type": "text",
                                            "text": {
                                                "content": "Price (IDR)",
                                                "link": None
                                            }
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                },
                {
                    "object": "block",
                    "type": "table_row",
                    "table_row": {
                        "cells": [
                            {
                                "object": "block",
                                "type": "table_cell",
                                "table_cell": {
                                    "rich_text": [
                                        {
                                            "type": "text",
                                            "text": {
                                                "content": "1",
                                                "link": None
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                "object": "block",
                                "type": "table_cell",
                                "table_cell": {
                                    "rich_text": [
                                        {
                                            "type": "text",
                                            "text": {
                                                "content": "Senggigi",
                                                "link": None
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                "object": "block",
                                "type": "table_cell",
                                "table_cell": {
                                    "rich_text": [
                                        {
                                            "type": "text",
                                            "text": {
                                                "content": "95.000",
                                                "link": None
                                            }
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                },
                {
                    "object": "block",
                    "type": "table_row",
                    "table_row": {
                        "cells": [
                            {
                                "object": "block",
                                "type": "table_cell",
                                "table_cell": {
                                    "rich_text": [
                                        {
                                            "type": "text",
                                            "text": {
                                                "content": "2",
                                                "link": None
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                "object": "block",
                                "type": "table_cell",
                                "table_cell": {
                                    "rich_text": [
                                        {
                                            "type": "text",
                                            "text": {
                                                "content": "Mataram",
                                                "link": None
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                "object": "block",
                                "type": "table_cell",
                                "table_cell": {
                                    "rich_text": [
                                        {
                                            "type": "text",
                                            "text": {
                                                "content": "95.000",
                                                "link": None
                                            }
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                },
                {
                    "object": "block",
                    "type": "table_row",
                    "table_row": {
                        "cells": [
                            {
                                "object": "block",
                                "type": "table_cell",
                                "table_cell": {
                                    "rich_text": [
                                        {
                                            "type": "text",
                                            "text": {
                                                "content": "3",
                                                "link": None
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                "object": "block",
                                "type": "table_cell",
                                "table_cell": {
                                    "rich_text": [
                                        {
                                            "type": "text",
                                            "text": {
                                                "content": "Lombok Airport",
                                                "link": None
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                "object": "block",
                                "type": "table_cell",
                                "table_cell": {
                                    "rich_text": [
                                        {
                                            "type": "text",
                                            "text": {
                                                "content": "195.000",
                                                "link": None
                                            }
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                },
                {
                    "object": "block",
                    "type": "table_row",
                    "table_row": {
                        "cells": [
                            {
                                "object": "block",
                                "type": "table_cell",
                                "table_cell": {
                                    "rich_text": [
                                        {
                                            "type": "text",
                                            "text": {
                                                "content": "4",
                                                "link": None
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                "object": "block",
                                "type": "table_cell",
                                "table_cell": {
                                    "rich_text": [
                                        {
                                            "type": "text",
                                            "text": {
                                                "content": "Kuta Lombok",
                                                "link": None
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                "object": "block",
                                "type": "table_cell",
                                "table_cell": {
                                    "rich_text": [
                                        {
                                            "type": "text",
                                            "text": {
                                                "content": "195.000",
                                                "link": None
                                            }
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                },
                {
                    "object": "block",
                    "type": "table_row",
                    "table_row": {
                        "cells": [
                            {
                                "object": "block",
                                "type": "table_cell",
                                "table_cell": {
                                    "rich_text": [
                                        {
                                            "type": "text",
                                            "text": {
                                                "content": "5",
                                                "link": None
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                "object": "block",
                                "type": "table_cell",
                                "table_cell": {
                                    "rich_text": [
                                        {
                                            "type": "text",
                                            "text": {
                                                "content": "Lembar",
                                                "link": None
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                "object": "block",
                                "type": "table_cell",
                                "table_cell": {
                                    "rich_text": [
                                        {
                                            "type": "text",
                                            "text": {
                                                "content": "195.000",
                                                "link": None
                                            }
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                },
                {
                    "object": "block",
                    "type": "table_row",
                    "table_row": {
                        "cells": [
                            {
                                "object": "block",
                                "type": "table_cell",
                                "table_cell": {
                                    "rich_text": [
                                        {
                                            "type": "text",
                                            "text": {
                                                "content": "6",
                                                "link": None
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                "object": "block",
                                "type": "table_cell",
                                "table_cell": {
                                    "rich_text": [
                                        {
                                            "type": "text",
                                            "text": {
                                                "content": "Senaru",
                                                "link": None
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                "object": "block",
                                "type": "table_cell",
                                "table_cell": {
                                    "rich_text": [
                                        {
                                            "type": "text",
                                            "text": {
                                                "content": "175.000",
                                                "link": None
                                            }
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                },
                {
                    "object": "block",
                    "type": "table_row",
                    "table_row": {
                        "cells": [
                            {
                                "object": "block",
                                "type": "table_cell",
                                "table_cell": {
                                    "rich_text": [
                                        {
                                            "type": "text",
                                            "text": {
                                                "content": "min 2 person",
                                                "link": None
                                            }
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                },
                {
                    "object": "block",
                    "type": "table_row",
                    "table_row": {
                        "cells": [
                            {
                                "object": "block",
                                "type": "table_cell",
                                "table_cell": {
                                    "rich_text": [
                                        {
                                            "type": "text",
                                            "text": {
                                                "content": "7",
                                                "link": None
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                "object": "block",
                                "type": "table_cell",
                                "table_cell": {
                                    "rich_text": [
                                        {
                                            "type": "text",
                                            "text": {
                                                "content": "Tete Batu",
                                                "link": None
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                "object": "block",
                                "type": "table_cell",
                                "table_cell": {
                                    "rich_text": [
                                        {
                                            "type": "text",
                                            "text": {
                                                "content": "250.000",
                                                "link": None
                                            }
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                },
                {
                    "object": "block",
                    "type": "table_row",
                    "table_row": {
                        "cells": [
                            {
                                "object": "block",
                                "type": "table_cell",
                                "table_cell": {
                                    "rich_text": [
                                        {
                                            "type": "text",
                                            "text": {
                                                "content": "min 2 person",
                                                "link": None
                                            }
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                },
                {
                    "object": "block",
                    "type": "table_row",
                    "table_row": {
                        "cells": [
                            {
                                "object": "block",
                                "type": "table_cell",
                                "table_cell": {
                                    "rich_text": [
                                        {
                                            "type": "text",
                                            "text": {
                                                "content": "8",
                                                "link": None
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                "object": "block",
                                "type": "table_cell",
                                "table_cell": {
                                    "rich_text": [
                                        {
                                            "type": "text",
                                            "text": {
                                                "content": "Padang Bai",
                                                "link": None
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                "object": "block",
                                "type": "table_cell",
                                "table_cell": {
                                    "rich_text": [
                                        {
                                            "type": "text",
                                            "text": {
                                                "content": "300.000",
                                                "link": None
                                            }
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                },
                {
                    "object": "block",
                    "type": "table_row",
                    "table_row": {
                        "cells": [
                            {
                                "object": "block",
                                "type": "table_cell",
                                "table_cell": {
                                    "rich_text": [
                                        {
                                            "type": "text",
                                            "text": {
                                                "content": "FASTBOAT",
                                                "link": None
                                            }
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                },
                {
                    "object": "block",
                    "type": "table_row",
                    "table_row": {
                        "cells": [
                            {
                                "object": "block",
                                "type": "table_cell",
                                "table_cell": {
                                    "rich_text": [
                                        {
                                            "type": "text",
                                            "text": {
                                                "content": "9",
                                                "link": None
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                "object": "block",
                                "type": "table_cell",
                                "table_cell": {
                                    "rich_text": [
                                        {
                                            "type": "text",
                                            "text": {
                                                "content": "Ubud, Sanur",
                                                "link": None
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                "object": "block",
                                "type": "table_cell",
                                "table_cell": {
                                    "rich_text": [
                                        {
                                            "type": "text",
                                            "text": {
                                                "content": "400.000",
                                                "link": None
                                            }
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                },
                {
                    "object": "block",
                    "type": "table_row",
                    "table_row": {
                        "cells": [
                            {
                                "object": "block",
                                "type": "table_cell",
                                "table_cell": {
                                    "rich_text": [
                                        {
                                            "type": "text",
                                            "text": {
                                                "content": "FASTBOAT",
                                                "link": None
                                            }
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                },
                {
                    "object": "block",
                    "type": "table_row",
                    "table_row": {
                        "cells": [
                            {
                                "object": "block",
                                "type": "table_cell",
                                "table_cell": {
                                    "rich_text": [
                                        {
                                            "type": "text",
                                            "text": {
                                                "content": "10",
                                                "link": None
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                "object": "block",
                                "type": "table_cell",
                                "table_cell": {
                                    "rich_text": [
                                        {
                                            "type": "text",
                                            "text": {
                                                "content": "Denpasar, Kuta",
                                                "link": None
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                "object": "block",
                                "type": "table_cell",
                                "table_cell": {
                                    "rich_text": [
                                        {
                                            "type": "text",
                                            "text": {
                                                "content": "450.000",
                                                "link": None
                                            }
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                },
                {
                    "object": "block",
                    "type": "table_row",
                    "table_row": {
                        "cells": [
                            {
                                "object": "block",
                                "type": "table_cell",
                                "table_cell": {
                                    "rich_text": [
                                        {
                                            "type": "text",
                                            "text": {
                                                "content": "FASTBOAT",
                                                "link": None
                                            }
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                },
                {
                    "object": "block",
                    "type": "table_row",
                    "table_row": {
                        "cells": [
                            {
                                "object": "block",
                                "type": "table_cell",
                                "table_cell": {
                                    "rich_text": [
                                        {
                                            "type": "text",
                                            "text": {
                                                "content": "11",
                                                "link": None
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                "object": "block",
                                "type": "table_cell",
                                "table_cell": {
                                    "rich_text": [
                                        {
                                            "type": "text",
                                            "text": {
                                                "content": "Sumbawa",
                                                "link": None
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                "object": "block",
                                "type": "table_cell",
                                "table_cell": {
                                    "rich_text": [
                                        {
                                            "type": "text",
                                            "text": {
                                                "content": "300.000",
                                                "link": None
                                            }
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                },
                {
                    "object": "block",
                    "type": "table_row",
                    "table_row": {
                        "cells": [
                            {
                                "object": "block",
                                "type": "table_cell",
                                "table_cell": {
                                    "rich_text": [
                                        {
                                            "type": "text",
                                            "text": {
                                                "content": "12",
                                                "link": None
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                "object": "block",
                                "type": "table_cell",
                                "table_cell": {
                                    "rich_text": [
                                        {
                                            "type": "text",
                                            "text": {
                                                "content": "Dompu",
                                                "link": None
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                "object": "block",
                                "type": "table_cell",
                                "table_cell": {
                                    "rich_text": [
                                        {
                                            "type": "text",
                                            "text": {
                                                "content": "350.000",
                                                "link": None
                                            }
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                },
                {
                    "object": "block",
                    "type": "table_row",
                    "table_row": {
                        "cells": [
                            {
                                "object": "block",
                                "type": "table_cell",
                                "table_cell": {
                                    "rich_text": [
                                        {
                                            "type": "text",
                                            "text": {
                                                "content": "13",
                                                "link": None
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                "object": "block",
                                "type": "table_cell",
                                "table_cell": {
                                    "rich_text": [
                                        {
                                            "type": "text",
                                            "text": {
                                                "content": "Bima",
                                                "link": None
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                "object": "block",
                                "type": "table_cell",
                                "table_cell": {
                                    "rich_text": [
                                        {
                                            "type": "text",
                                            "text": {
                                                "content": "400.000",
                                                "link": None
                                            }
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                },
                {
                    "object": "block",
                    "type": "table_row",
                    "table_row": {
                        "cells": [
                            {
                                "object": "block",
                                "type": "table_cell",
                                "table_cell": {
                                    "rich_text": [
                                        {
                                            "type": "text",
                                            "text": {
                                                "content": "14",
                                                "link": None
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                "object": "block",
                                "type": "table_cell",
                                "table_cell": {
                                    "rich_text": [
                                        {
                                            "type": "text",
                                            "text": {
                                                "content": "Sape",
                                                "link": None
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                "object": "block",
                                "type": "table_cell",
                                "table_cell": {
                                    "rich_text": [
                                        {
                                            "type": "text",
                                            "text": {
                                                "content": "500.000",
                                                "link": None
                                            }
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                },
                {
                    "object": "block",
                    "type": "table_row",
                    "table_row": {
                        "cells": [
                            {
                                "object": "block",
                                "type": "table_cell",
                                "table_cell": {
                                    "rich_text": [
                                        {
                                            "type": "text",
                                            "text": {
                                                "content": "15",
                                                "link": None
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                "object": "block",
                                "type": "table_cell",
                                "table_cell": {
                                    "rich_text": [
                                        {
                                            "type": "text",
                                            "text": {
                                                "content": "Labuan Bajo",
                                                "link": None
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                "object": "block",
                                "type": "table_cell",
                                "table_cell": {
                                    "rich_text": [
                                        {
                                            "type": "text",
                                            "text": {
                                                "content": "550.000",
                                                "link": None
                                            }
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                }
            ]
        }
    },
    {
        "object": "block",
        "type": "heading_2",
        "heading_2": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": "Additional Notes",
                        "link": None
                    }
                }
            ],
            "color": "default",
            "is_toggleable": False
        }
    },
    {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": "Leave from Gili Meno time is at 08:00 AM",
                        "link": None
                    }
                }
            ],
            "color": "default"
        }
    }
])
