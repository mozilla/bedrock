#!/bin/bash -xe

exec supervisord -c etc/supervisord.conf
