# Beer Temperature Monitor

A Python service that relays a Raspberry Pi temperature to an external service for processing.

More info to come later!

# Requirements
- Raspberry Pi (current development on Raspberry Pi Zero)
- Adafruit MCP9808 Temperature sensor
- Virtualenv

# Prerequisites
## Python virtualenv
Running this project becomes infinitely easier when run in a virtual environment.

Install virtualenv (assuming you have access to python3):

    $> python3 -m venv venv

Once virtualenv is installed, activate it:
    
    $> source venv/bin/activate

From here, you should be able to follow the `Install` section.

# Install
1. Download repo
2. Go into project folder
  - cd beer_temp_monitor
3. Install required packages
  - pip install -r requirements.txt
4. Run the monitor! (Currently, receiving server must be up and running!)
  - python src/beer_temp_monitor.py


# Auto Start
This project is meant to run on the Pi at boot, without intervention. To that end, I currently use `systemd` to start the program on boot.

Details on how to accomplish this can be found [here][1] and [here][2].

I thought I'd share some particulars on the systemd service file that 
eventually worked for me. In the following service file:


    [Unit]
    Description=Beer Monitor Service
    After=multi-user.target

    [Service]
    Type=forking
    User=pi
    ExecStart=/bin/bash /home/pi/scripts/beer-monitor.sh > /home/pi/    service-logs/monitor.log 2>&1

    [Install]
    WantedBy=multi-user.target

`Type` was set to `forking`, because I run this project in a detched 
screen. My previous attempt had it set to `simple`. It failed, however,
because `simple` tells systemd that the main process is meant to run
forever. In contrast, Screen is doing the opposite; it starts a new
session and forks to background. Details on how I discovered this can be
read in the answer found [here][3].

I wanted to run this script, and ultimately the project, as the user
that the pi is setup on, so `User` is set to `pi_user`, where `pi_user`
is whatever your user is.


[1]: https://www.raspberrypi.org/documentation/linux/usage/systemd.md
[2]: http://neilwebber.com/notes/2016/02/10/making-a-simple-systemd-file-for-raspberry-pi-jessie/
[3]: https://superuser.com/questions/1276775/systemd-service-python-script-inside-screen-on-boot