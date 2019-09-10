#!/usr/bin/env bash
set -ex

# 换源
# 不用在服务器执行这个脚本
cp /var/www/web21/misc/sources.list /etc/apt/sources.list
mkdir -p /root/.pip
cp /var/www/web21/misc/pip.conf /root/.pip/pip.conf
apt-get update