import click
from graviteeio_cli.http_client.apim.api import ApiClient

from ....exeptions import GraviteeioError


@click.command()
@click.option('--api', 'api_id',
              help='API id',
              required=True)
@click.pass_obj
def start(obj, api_id):
    """Starts an API."""
    api_client: ApiClient = obj['api_client']
    try:
        api_client.start(api_id)
    except GraviteeioError:
        click.echo("Error: " + click.style("API [{}] could not be started.".format(api_id), fg="red"))

    click.echo("API [{}] is started.".format(api_id))
