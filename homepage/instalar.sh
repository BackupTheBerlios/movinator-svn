#!/bin/sh

# Script para instalar a pagina, usando o rsync.

# Ficheiros a copiar
TO_SYNC=(\
    . \
)

# Lista de ficheiros a n�o copiar
EXCLUDE=exclude

# Ender�o remoto
REMOTE=caladopc@shell.berlios.de:/home/groups/movinator/htdocs

# Op��es do rsync
OPTIONS=(\
    --checksum \
    --recursive \
    --links \
#    --perms \ # nao funciona no Berlios
#    --times \ # nao funciona no Berlios
    --one-file-system \
    --compress \
    --stats \
    --progress \
    --rsh=ssh \
    --delete \
#    --delete-excluded \ # nao funciona no Berlios
    --cvs-exclude \
)

rsync ${OPTIONS[*]} ${TO_SYNC[*]} $REMOTE --exclude-from=$EXCLUDE
