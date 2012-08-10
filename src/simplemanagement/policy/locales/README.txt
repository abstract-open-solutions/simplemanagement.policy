This directory will contains translation directories and respective .po and .mo files.

For each necessary language you should create a directory called with the name of language you want to translate this product:

    * it/LC_MESSAGES
    * fr/LC_MESSAGES
    * en_GB/LC_MESSAGES
    * ...

and launch rebuild.sh script.
This script will create a .pot file in this directory and create or update corresponding .po file in each language directory.

IMPORTANT:
Before launching rebuild.sh you must replace $PRODUCT variable with the name of the package you want translate.
