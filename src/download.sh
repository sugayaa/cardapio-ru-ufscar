#!/bin/bash

FOLDER=/tmp/cardapio-ru/
FILE=ru.html
FILEPATH=$FOLDER$FILE

#if file is more than 6 days old, delete it
find $FILEPATH -mtime +6 -type f 2>/dev/null

if [ ! -d $FOLDER ] && [ ! -f $FILEPATH ]; then
    mkdir $FOLDER
    curl -s https://www2.ufscar.br/restaurantes-universitario/cardapio > $FILEPATH
elif [ ! -f $FILEPATH ]; then
    curl -s https://www2.ufscar.br/restaurantes-universitario/cardapio > $FILEPATH
fi
