#!/usr/bin/env bash

CONF_DIR="/frp/conf"
CONF_FILE=${FRP_CONF_FILE:-"frps.toml"}
CONF_PATH="$CONF_DIR/$CONF_FILE"
RUN_MODE=${RUN_MODE:-"server"}

# check conf file
if [ ! -f "$CONF_PATH" ]; then
    echo "Configuration file $CONF_PATH not found!"
    exit 1
fi

echo "frp version is $FRP_VERSION"

cd /frp/bin

if [ "$RUN_MODE" = "server" ]; then
    echo "Running frp server with config: $CONF_PATH"
    ./frps -c "$CONF_PATH"
elif [ "$RUN_MODE" = "client" ]; then
    echo "Running frp client with config: $CONF_PATH"
    ./frpc -c "$CONF_PATH"
else
    echo "Invalid RUN_MODE. Please specify either 'server' or 'client'."
    exit 1
fi