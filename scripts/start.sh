#!/bin/sh

set -e
echo "*************** Main Process - SQLApify client starting ..... ************ "

if [ "$SQLAPIFY_ENV" = "dev" ]; then
    echo "*************** Loading $SQLAPIFY_ENV env file ************ "
    exec uvicorn src.main:app --host $SQLAPIFY_HOST --port $SQLAPIFY_PORT --env-file  $VIRTUAL_ENV/env/.env.$BUILD_TARGET.$SQLAPIFY_ENV
else
    exec uvicorn src.main:app --host $SQLAPIFY_HOST --port $SQLAPIFY_PORT
fi