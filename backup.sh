#!/bin/sh
# backup.sh
# Sauvegarde complète de la base de données PostgreSQL
pg_dumpall -U ${POSTGRES_USER} -h ${POSTGRES_HOST} > /var/backups/postgresql/backup_full_$(date +%Y-%m-%d_%H-%M-%S).sql