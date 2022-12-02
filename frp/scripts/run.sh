#!/usr/bin/env bash

cd /frp/bin
frps_conf_path=/frp/conf/frps.ini
frpc_conf_path=/frp/conf/frpc.ini

echo "frp version is $FRP_VERSION"

case $RUN_MODE in
    "server") ./frps -c $frps_conf_path
    ;;
    "client") ./frpc -c $frpc_conf_path
    ;;
    *) 
    if [ -f $frps_conf_path ]; then
        ./frps -c $frps_conf_path
    elif [-f $frpc_conf_path ]; then
        ./frpc -c $frpc_conf_path
    else
        echo "Please set the running mode of frp with RUN_MODE."
    fi
    ;;
esac