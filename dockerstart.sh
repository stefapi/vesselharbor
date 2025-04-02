#!/bin/sh
set -e

echo "Starting backend..."
uvicorn main:app --host 0.0.0.0 --port 8010 &

echo "Starting frontend..."
# 'serve' va servir les fichiers statiques du frontend
serve -s /app/frontend/dist -l 5000 &

echo "Starting Caddy..."
caddy run --config /etc/caddy/Caddyfile &

# Attend la fin d'un des processus
wait -n
echo "A process has exited. Shutting down..."
exit 1

