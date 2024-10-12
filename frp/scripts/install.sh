#!/bin/bash

# extract frp files
mkdir -p bin && cd bin
tar zxf ../frp_${FRP_VERSION}_linux_amd64.tar.gz -C . --strip-components=1

# move conf files
mkdir -p ../conf && mv *.toml ../conf

# create version file
touch $FRP_VERSION
ls -l
