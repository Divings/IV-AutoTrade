#!/usr/bin/bash

#yum makecache
systemctl stop fx-autotrade.service
yum update $1 -y
systemctl restart fx-autotrade.service