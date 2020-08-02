# pi_temp

pi_temp offers means to view and log the core temperature of a RPi CPU.

Functionality includes: 
  - the ability to change the rate measurements of the CPU temperature are taken, 
  - the ability to choose the location for pi_temp logs,
  - the ability to run pi_temp from any directory with an alias, and
  - the ability to use pi_temp as a systemd service (run at boot).

# Install Guide:

Extract the contents of the tarball:

    $ tar -xvzf pi_temp_v1.gz

Change directories into the pi_temp_v1 directory:

    $ cd pi_temp_v1

Run the install script.  install.sh will will create and configure the ~/pi_temp directory and files as well as the pi_temp.service file and pi_temp alias.  The bash install script will offer the option to change the install location (hit RETURN to use default configuration).

    $ ./install.sh

Simple test. 

    $ pitemp -r

You should see something like:

    08/02/20 16:58:23 - 115.1 F /47.2 C

    (Logs are going to /home/pi/pi_temp/pi_temp.log)

That's it! You're up and running.

# Explore options:

    $ pitemp                <-- runs with default config (60s)
    $ pitemp -h             <-- shows help
    $ pitemp -s 2           <-- run with a sample time of 2s
    $ pitemp -p /usb -s 30  <-- logs to /usb/pi_temp.log every 30 s
    $ pitemp -r             <-- get and logs the current CPU temp
    $ pitemp -i             <-- verify current default
    $ pitemp -v             <-- shows version installed
