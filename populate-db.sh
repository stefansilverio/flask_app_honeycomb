#!/usr/bin/env bash
set -x

SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

PORT=3000
APIURL="http://127.0.0.1:5000/api"
USERNAME="tomi"
EMAIL="admin@admin.com"
PASSWORD="Abcd123$"
MAX_COMMENT_COUNT=50

npx newman run $SCRIPTDIR/Conduit.postman_collection.json \
  --delay-request 50 \
  --global-var "APIURL=$APIURL" \
  --global-var "USERNAME=$USERNAME" \
  --global-var "EMAIL=$EMAIL" \
  --global-var "PASSWORD=$PASSWORD" \
  --global-var "MAX_COMMENT_COUNT=$MAX_COMMENT_COUNT"
