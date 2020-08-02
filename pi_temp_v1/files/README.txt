
PPPPPPP                  TTT    
PPPPPPPP                 TTT                        
PPP  PPP  III        TTTTTTTTTTTT   EEEEEE   MMM          PPPPPP   
PPPPPPPP  III        TTTTTTTTTTTT  EEE  EEE  MMMMMMMMMMM  PPPPPPPP    
PPPPPPP                  TTT      EEEEEEEEE  MMM  MM  MM  PPP   PP   
PPP       III            TTT      EE         MMM  MM  MM  PPPPPPPP    
PPP       III            TTT      EE     EE  MMM  MM  MM  PPPPPPP      
PPP       III            TTT       EEEEEEE   MMM  MM  MM  PPP     
PPP       III  DDDDDDD   TTT        EEEEE    MMM  MM  MM  PPP    
 
     


If correct install - 'pi_temp' and 'pitemp' aliases should exist.

    $ python3 /home/pi/pi_temp/pi_temp.py
    $ pi_temp
    $ pitemp

Examples:

    $ pitemp			<-- runs with default config (60s)
    $ pitemp -h 		<-- shows help
    $ pitemp -s 2               <-- run with a sample time of 2s
    $ pitemp -p /usb -s 30	<-- logs to /usb/pi_temp.log every 30 s
    $ pitemp -r                 <-- get and logs the current CPU temp
    $ pitemp -i                 <-- verify current default config
    $ pitemp -v 		<-- shows version installed
   

To change the sample time (time between measurements) and to change the
    location that logs are saved:
    $ nano ~/pi_temp.conf               <-- with the default install

To watch the temperature measurements in real time:
    $ tail -f ~/pi_temp/pi_temp.log     <-- with the default install

To start pi_temp as a service:
    $ sudo systemctl start pi_temp.service

To have pi_temp start on boot:
    $ sudo systemctl enable pi_temp.service



