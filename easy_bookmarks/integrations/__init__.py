from easy_bookmarks.integrations.linkedin import LinkedinIntegration
from easy_bookmarks.integrations.webpage import PwCWebpageIntegration


INTEGRATION_MAP = {
    "linkedin": LinkedinIntegration,
    "PapersWithCode": PwCWebpageIntegration,
}


def get_integration(integration_name: str):
    if integration_name not in INTEGRATION_MAP:
        raise ValueError(
            f"""
        Integration {integration_name} not found.
        Please check your config file and the INTEGRATION_MAP in integrations/__init__.py.
        """
        )
    return INTEGRATION_MAP[integration_name]
