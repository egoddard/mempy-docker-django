#!/bin/bash

if [ -z $USER_ID ]; then
  USER_ID=1000
fi

useradd --shell /bin/bash -u $USER_ID -o -c "" -m user
export HOME=/home/user

chown -R user:user /app

exec /usr/local/bin/gosu user "$@"