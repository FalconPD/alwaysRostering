# Atlas Scripts

## Overview

This directory contains scripts used to keep Atlas in sync with the information
in Genesis. Currently Atlas does not have a means of storing the Genesis ID so
users are matched by (in order of precedence):

1. Their userid email address
2. Their first and last names
3. Their first name and former (maiden) last name

It should also be noted that Atlas allows users to have multiple emails, so a
user may report that they can still log in with their old FirstName.LastName
email address.

## users.py

```console
Usage: users.py [OPTIONS] DB_FILE

  Syncs Atlas user accounts with Genesis database file DB_FILE

Options:
  --debug  Print debugging statements
  --help   Show this message and exit.
```
