#!/bin/sh

COMMAND='python /home/pi/repos/Beer-Temp-Monitor/beer_temp_mon.py'
LOGFILE='restart.txt'

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
