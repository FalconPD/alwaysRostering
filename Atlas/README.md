# sync_atlas.py

## Overview

This script provides a command line interface to keep Atlas in sync with the
information in Genesis. It uses a CSV map_file to keep track of how Atlas IDs
correspond to Genesis IDs (Atlas does not current support storing a school ID).
For all actions performed by this script the id_map should be maintained
automatically. It can be recreated (to the best of its ability) by using the
create_map command.

## Usage
```
Usage: sync_atlas.py [OPTIONS] DB_FILE MAP_FILE COMMAND1 [ARGS]... [COMMAND2
                     [ARGS]...]...

  Loads the Genesis database from DB_FILE and the Atlas to Genesis ID map
  from MAP_FILE before performing COMMAND(s).

Options:
  --debug  Print debugging statements
  --help   Show this message and exit.

Commands:
  create_map  create id map based on first and last names
  sync_users  sync up user accounts
```
