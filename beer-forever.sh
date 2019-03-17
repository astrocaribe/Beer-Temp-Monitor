#!/usr/bin/env bash

COMMAND='python src/beer_temp_monitor.py'
LOGFILE='logs/restart.txt'

writelog() {
    now=`date`
    echo "$now $*" >> $LOGFILE
}

writelog "Starting server..."
while true ; do
  $COMMAND
  writelog "Exited with status $?"
  writelog "Restarting server..."
  writelog "--------------------"
  writelog ""
done