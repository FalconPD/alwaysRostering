import asyncio
import click
import logging

import AR.nwea_map as nwea_map

async def perform_actions(standard, additional, status):
    async with nwea_map.Session() as map_session: 
        if standard:
            print(f"Uploading standard roster: {standard}")
            print(await map_session.upload_standard(standard))
        
        if additional:
            print(f"Uploading additional users roster: {additional}")
            print(await map_session.upload_additional(additional))

        if status:
            print("Status:")
            print(await map_session.status())
            print("Errors:")
            print(await map_session.errors())

@click.command()
@click.option('--debug', help="turn on debugging", is_flag=True)
@click.option('--standard', help="standard roster", type=click.Path(exists=True))
@click.option('--additional', help="additional roster", type=click.Path(exists=True))
@click.option('--status', help="print status", is_flag=True)
def cli(debug, standard, additional, status):
    """
    Uploads a standard and/or additional roster to NWEA MAP. Optionally prints
    status and errors as well.
    """
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARNING)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(perform_actions(standard, additional, status))

if __name__ == '__main__':
    cli()
