import click

from .apis.apis import apis
from .auth.auth import auth
from graviteeio_cli.graviteeio.modules import GraviteeioModule

@click.group(invoke_without_command=False)
@click.pass_context
def apim(ctx):
    "Api Management commands"
    ctx.obj['module'] = GraviteeioModule.APIM
    pass


apim.add_command(apis)
apim.add_command(auth)
