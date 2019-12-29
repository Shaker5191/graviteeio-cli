import time

import click
import jmespath

from graviteeio_cli.graviteeio.output import FormatType, OutputFormat, gio
from pytimeparse import parse

from ....exeptions import GraviteeioError

colors = {"1xx":"white","2xx":"green","3xx":"white","4xx":"yellow","5xx":"red"}

@click.command()
@click.argument('api_id', required=True)
@click.option('-f','--format',
              default="table",
              help='Set the format for printing command output resources. The supported formats are: `table`, `json`, `yaml`, `tsv`. Default is: `table`',
              type=click.Choice(FormatType.list_name(), case_sensitive=False))
@click.option('-q','--query',
              default="[].{Status: status, Hits: hits, Percent: percent}",
              help='Execute JMESPath query. Default: `[].{Status: status, Hits: hits, Percent: percent}` eg: filtered on 5xx status `[?status==`5xx`].{Status: status, Hits: hits, Percent: percent}`' )
@click.option('-tf','--time-frame',
              default="5m",
              help="Timeframe between now and the vale. Default: `5m`. m -> minute, h -> hour, d -> days")
@click.pass_obj
def status(obj, format, query, time_frame, api_id):
    """
This command displays API status

\b
Status Field:
- `status`: string 
- `hits`: numerate
- `percent`: string
    """
    api_client = obj['api_client']

    try: 
        status_values = api_client.status(api_id, parse(time_frame)).json()['values']
    except TypeError:
        raise GraviteeioError("Unsupported type for time frame")

    to_return = []
    total = 0
    for key,value in status_values.items():
        status_str = "{}xx".format(key[0:1])
        to_return.append(
            {
                "status": status_str,
                "hits": value,
                "percent": value * 100
            }
        )
        total += value

    if total > 0:
        for status in to_return:
            status["percent"] = round(status["percent"] / total, 2)
 
    # start_time = time.time()
    try:
        status_filtered = jmespath.search(query, to_return)
    
        if len(to_return) > 0:
            header = status_filtered[0].keys()
            
        outputFormat = OutputFormat.value_of(format)
        gio.echo(status_filtered, outputFormat, header)

    except Exception as err:
        raise GraviteeioError(err.msg)
