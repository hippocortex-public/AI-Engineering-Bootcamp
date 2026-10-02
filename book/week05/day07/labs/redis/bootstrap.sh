#!/bin/sh
set -eu
umask 077
cat > /tmp/bootcamp-redis.conf <<'CONF'
bind 0.0.0.0
protected-mode yes
dir /data
appendonly yes
appendfsync everysec
maxmemory 128mb
maxmemory-policy noeviction
CONF
printf 'requirepass %s\n' "$(cat /run/secrets/redis_password)" >> /tmp/bootcamp-redis.conf
chown redis:redis /tmp/bootcamp-redis.conf
exec docker-entrypoint.sh redis-server /tmp/bootcamp-redis.conf
