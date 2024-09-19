import os

import click
import yaml
from dotenv import load_dotenv

from easy_bookmarks.integrations import get_integration
from easy_bookmarks.stores import get_store

load_dotenv()


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "--config", "-c", type=click.Path(exists=True), help="Path to config file"
)
def run(config):
    if config:
        with open(config, "r") as f:
            config_data = yaml.safe_load(os.path.expandvars(f.read()))
    else:
        raise ValueError("Config file not found")

    store_name = list(config_data["store"].keys())[0]
    store_metadata = config_data["store"][store_name]

    for integration_name in config_data["integrations"].keys():
        store = get_store(store_name)(
            **{"config": store_metadata["config"]},
            **store_metadata["databases"][integration_name],
        )
        integration_instance = get_integration(integration_name)(
            **config_data["integrations"][integration_name]
        )
        click.echo(f"Fetching {integration_name} bookmarks")
        try:
            df_bookmarks = integration_instance.get_bookmarks_df()
            click.echo(f"Storing {integration_name} bookmarks")
            store.add_bookmarks_from_df(df_bookmarks)
            click.echo("Bookmarks stored")
        except Exception as e:
            click.echo(f"Error fetching {integration_name} bookmarks: {e}")


if __name__ == "__main__":
    cli()
