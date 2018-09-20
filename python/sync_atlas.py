import AR.atlas as atlas
import click
import asyncio
import logging

@click.command()
@click.argument('db_file', type=click.Path(exists=True), metavar='DB_FILE')
@click.option("--debug", is_flag=True, help="Print debugging statements")
def main(db_file, debug):
    """
    Syncs up Rubicon Atlas with a Genesis Database

    DB_FILE - A sqlite3 file of the Genesis database
    """
    loop = asyncio.get_event_loop()

    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARNING)

    loop.run_until_complete(sync(loop=loop, db_file=db_file))
    loop.close()

async def sync(loop, db_file):
    """
    Performs all steps to sync Atlas with a Genesis Database
    """
    async with atlas.Session() as Atlas:
        print("Done")

if __name__ == '__main__':
    main()
