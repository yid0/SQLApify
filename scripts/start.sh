#!/bin/sh

set -e
echo "*************** Main Process - SQLApify client starting ..... ************ "

exec uvicorn src.main:app --host $SQLAPIFY_HOST --port $SQLAPIFY_PORT --env-file  $VIRTUAL_ENV/env/.env.$BUILD_TARGET.$SQLAPIFY_ENV --lifespan on
