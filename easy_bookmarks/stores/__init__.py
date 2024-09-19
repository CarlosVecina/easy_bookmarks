from easy_bookmarks.stores.notion_store import NotionStore


STORE_MAP = {
    "notion": NotionStore,
}


def get_store(store_name: str):
    if store_name not in STORE_MAP:
        raise ValueError(
            f"""
        Store {store_name} not found.
        Please check your config file and the STORE_MAP in stores/__init__.py.
        """
        )
    return STORE_MAP[store_name]
