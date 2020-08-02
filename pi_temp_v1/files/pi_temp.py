#!/usr/bin/python3

# RPi core temperature logging
# python3
# D483

# Notes:
# ---------------------------------------------------------
# Max temp is 80C or 176F
# Dangerous temp of 60C is 140F
#
# To change core temperature sample rate edit:
# ~/pi_temp/pi_temp.conf
#
# Logs for core templerature history are by default at:
# ~/pi_temp/pi_temp.log
#
# Service config file at:
# /etc/systemd/system/pi_temp.service
# ---------------------------------------------------------

import os
import datetime
import configparser
import argparse
import logging
import textwrap
from sys import argv
from gpiozero import CPUTemperature
from time import sleep, time


def get_config():

    # sample time is pulled from the .conf file
    config = configparser.ConfigParser()
    config.read('/home/pi/pi_temp/pi_temp.conf')
    Sample = int(config['Settings']['Sample_time'])
    Log_path = str(config['Settings']['Log_Path'])

    return Sample, Log_path

def get_temp():

    # Returns a tuple with core temperature in Fahrenheit and Celcius (with only one decimal place)
    TempC = str(round(CPUTemperature().temperature,1))
    TempF = str(round(((CPUTemperature().temperature * 9 / 5) + 32 ),1))
    return(TempF,TempC)

def get_DTG():

    # Returns a string with the current datetime stamp
    # The format is: DD/MM/YY HH:MM:SS

    Dtg = str(datetime.datetime.now().strftime("%x %X"))
    return Dtg

def print_and_log():

    # Prints and logs the current datetime stamp and temperature
    # The format is:  DD/MM/YY HH:MM:SS - XX.X F / XX.X C

    TempF, TempC = get_temp()
    Current_Time = get_DTG()
    Log_String = Current_Time + " - " + TempF + " F / " + TempC + " C"

    print(Log_String)
    logging.info(Log_String)

def main():

    # establish sample time and path
    SAMPLE_TIME, PATH = get_config()

    print(f'path is {PATH}')

    # Change current directory to PATH found in pi_temp.conf
    os.chdir(PATH)

    # Parse arguments at run time
    parser = argparse.ArgumentParser(f"python3 {PATH}/pi_temp.py", epilog=textwrap.dedent('''\

            To change the sample time (time between measurements) and to change the
                location that logs are saved:
                $ nano ~/pi_temp.conf               <-- with the default install

            To watch the temperature measurements in real time:
                $ tail -f ~/pi_temp/pi_temp.log     <-- with the default install

            To start pi_temp as a service:
                $ sudo systemctl start pi_temp.service

            To have pi_temp start on boot:
                $ sudo systemctl enable pi_temp.service

            If correct install - 'pi_temp' and 'pitemp' aliases should exist.

                $ pitemp                    <-- runs with default config (60s)
                $ pitemp -h                 <-- shows help
                $ pitemp -r                 <-- get and log the current CPU temp
                $ pitemp -s 2               <-- run with a sample time of 2s
                $ pitemp -p /usb -s 30      <-- logs to /usb/pi_temp.log every 30 s
                $ pitemp -i                 <-- verify current default config
                $ pitemp -v                 <-- shows version installed

            To download from github:
                see D48E/pi_temp

            .
  '''), formatter_class=argparse.RawDescriptionHelpFormatter, description=textwrap.dedent('''\
PPPPPPP                  TTT
PPPPPPPP                 TTT
PPP  PPP  III        TTTTTTTTTTTT   EEEEEE   MMM          PPPPPP
PPPPPPPP  III        TTTTTTTTTTTT  EEE  EEE  MMMMMMMMMMM  PPPPPPPP
PPPPPPP                  TTT      EEEEEEEEE  MMM  MM  MM  PPP   PP
PPP       III            TTT      EE         MMM  MM  MM  PPPPPPPP
PPP       III            TTT      EE     EE  MMM  MM  MM  PPPPPPP
PPP       III            TTT       EEEEEEE   MMM  MM  MM  PPP
PPP       III  DDDDDDD   TTT        EEEEE    MMM  MM  MM  PPP
                    '''))


    parser.add_argument("-r", "--read", action="store_true", help="reads Pi core CPU temperature one time")
    parser.add_argument("-i", "--info", action="store_true", help="returns current configuration settings")
    parser.add_argument("-v", "--version", action="store_true", help="returns pi_temp version and quits.")
    parser.add_argument("-p", "--path", action="store", type=str, default="default", help="changes the path where logs are stored, this time only")
    parser.add_argument("-s", "--sample", action="store", type=int, help="changes the time between measurements (in seconds), this time only")

    args = parser.parse_args()


    # GET current configuration settings

    if (args.info):
        LOG_PATH = PATH+"pi_temp.log"
        print("\nCurrent configuration in pi_temp.conf")
        print("---------------------------------------------------------")
        print(f"  Sample time:         {SAMPLE_TIME}")
        print(f"  Logs are stored at:  {LOG_PATH}")
        print("---------------------------------------------------------\n")
        quit()

    # GET current version

    if (args.version):
        print("\nVersion 1.0\n")
        quit()

    # Option to change path to pi_temp.log (pi_temp.conf is NOT changed)

    if (args.path != "default"):
        PATH = args.path
        logging.basicConfig(filename=f'{PATH}pi_temp.log', filemode='a', format='%(message)s', level=logging.DEBUG)
    else:
        logging.basicConfig(filename=f'{PATH}pi_temp.log', filemode='a', format='%(message)s', level=logging.DEBUG)

    # Option to control sampling time - this time only

    if (args.sample != None):
        SAMPLE_TIME = args.sample

    # Option to read Pi core CPU temperature one time only

    if (args.read):
        print("")
        print_and_log()
        print(f'\n(Logs are going to {PATH}pi_temp.log)')
        quit()
    else:
        print(f'\n(Logs are going to {PATH}pi_temp.log)')
        print(f'(Sample time is {SAMPLE_TIME} seconds.)\n')

    # Monitoring Loop

    while True:
        print_and_log()
        sleep(SAMPLE_TIME)

if __name__ == "__main__":

    main()
