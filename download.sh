#!/bin/bash

#if file is more than 6 days old, delete it
find ru.html  -mtime +6 -type f -delete

if [ ! -f ru.html ]; then
    curl https://www2.ufscar.br/restaurantes-universitario/cardapio > ru.html
else
    echo "File is found and useful! Not downloading again"
fi
