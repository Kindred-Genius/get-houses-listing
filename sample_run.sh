#!/bin/bash

RUN_USER=ubuntu
EXEC_CMD=/home/ubuntu/project/get-houses-listing/run.sh

/bin/su ${RUN_USER} -c "{EXEC_CMD} $* &"
