#!/usr/bin/env bash

# Deployment script - intended to run on unim-leaderboard server

# Colors
C_RESET='\033[0m'
C_RED='\033[1;31m'
C_GREEN='\033[1;32m'
C_YELLOW='\033[1;33m'

# Logs
PREFIX_INFO="${C_GREEN}[INFO]${C_RESET} [$(date +%d-%m\ %T)]"
PREFIX_WARN="${C_YELLOW}[WARN]${C_RESET} [$(date +%d-%m\ %T)]"
PREFIX_CRIT="${C_RED}[CRIT]${C_RESET} [$(date +%d-%m\ %T)]"

# Main
APP_DIR="${APP_DIR:-/home/ubuntu/unim-leaderboard}"
SCRIPT_DIR="$(realpath $(dirname $0))"
SECRETS_DIR="${SECRETS_DIR:-/home/ubuntu/unim-leaderboard-secrets}"
PARAMETERS_ENV_PATH="${SECRETS_DIR}/app.env"

# Service file
SERVICE_FILE="unimleaderboard.service"

set -eu

echo
echo
echo -e "${PREFIX_INFO} Setting parameters"
if [ ! -d "$SECRETS_DIR" ]; then
  mkdir "$SECRETS_DIR"
  echo -e "${PREFIX_WARN} Created new secrets directory" 
fi
echo "UNIM_LEADERBOARD_PORT=8080" > "$PARAMETERS_ENV_PATH"

echo
echo
echo -e "${PREFIX_INFO} Building project with npm"
npm install --prefix "${APP_DIR}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing unim-leaderboard server definition with ${SERVICE_FILE}"
chmod 644 "${SCRIPT_DIR}/${SERVICE_FILE}"
cp "${SCRIPT_DIR}/${SERVICE_FILE}" "/etc/systemd/system/${SERVICE_FILE}"
systemctl daemon-reload
systemctl restart "${SERVICE_FILE}"
systemctl status "${SERVICE_FILE}"
