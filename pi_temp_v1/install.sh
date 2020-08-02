#!/bin/bash

RED='\033[0;31m'
CYAN='\033[0;36m'
YELLOW='\033[0;33m'
DEFAULT='\033[0m'
SUCCESS=0

echo -e "$CYAN\nInstalling pi_temp ...\n$DEFAULT"

USERHOME=$HOME

if [ "$?" = "0" ]; then
	echo -e  "$CYAN[+]$DEFAULT Home directory found: $USERHOME"
else
	echo -e  "$RED[+]$DEFAULT Failed to aquire home directory"
	SUCCESS=1
fi

# get home directory 
echo ""
PROMPT="Enter your install directory [$USERHOME]: "
read -p "$PROMPT" DIRECTORY
USERHOME=${DIRECTORY:-$USERHOME}
echo ""

# create pi_temp directory 
mkdir -p $USERHOME/pi_temp/

if [ "$?" = "0" ]; then
	echo -e  "$CYAN[+]$DEFAULT Directory stucture created successfully. $USERHOME/pi_temp"
else
	echo -e  "$RED[+]$DEFAULT Failed to create $USERHOME/test/test file directory"
	SUCCESS=1
fi

# move pi_temp.py

sudo cp files/pi_temp.py $USERHOME/pi_temp/

if [ "$?" = "0" ]; then
	echo -e  "$CYAN[+]$DEFAULT pi_temp.py copied."

	before="config.read('/home/pi/pi_temp"
	after="config.read('${USERHOME}/pi_temp"

	sed -i "s|$before|$after|g" $USERHOME/pi_temp/pi_temp.py 2>/dev/null


	if [ "$?" = "1" ]; then
		echo -e  "$RED[+]$DEFAULT Error configuring $USERHOME/pi_temp/pi_temp.py"
		SUCCESS=1
	fi
else
	echo -e  "$RED[+]$DEFAULT pi_temp.py not copied."
	SUCCESS=1
fi

# move pi_temp.log

cp files/pi_temp.log $USERHOME/pi_temp/

if [ "$?" = "0" ]; then
	echo -e  "$CYAN[+]$DEFAULT pi_temp.log copied"

else
	echo -e  "$RED[+]$DEFAULT pi_temp.log not copied"
	SUCCESS=1
fi


# move pi_temp.conf

cp files/pi_temp.conf $USERHOME/pi_temp/

if [ "$?" = "0" ]; then
	echo -e  "$CYAN[+]$DEFAULT config file found at ${after:13}/pi_temp.conf"


	before="Log_path = /home/pi/pi_temp"
	after="Log_path = ${USERHOME}/pi_temp"

	sed -i "s|$before|$after|g" $USERHOME/pi_temp/pi_temp.conf 2>/dev/null
	

	if [ "$?" = "0" ]; then
		echo -e  "$CYAN[+]$DEFAULT logs found at ${after:11}/pi_temp.log."
	else
		echo -e  "$RED[+]$DEFAULT Error adjusting Log_path in $USERHOME/pi_temp/pi_temp.conf"
		SUCCESS=1
	fi


else
	echo -e  "$RED[+]$DEFAULT pi_temp.conf not copeied."
	SUCCESS=1
fi

cp files/README.txt $USERHOME/pi_temp/

if [ "$?" = "0" ]; then
	echo -e  "$CYAN[+]$DEFAULT README.txt copied."
else
	echo -e  "$RED[+]$DEFAULT README.txt not copied."
	SUCCESS=1
fi

# chmod 555 pi_temp.py 

sudo chmod 555 $USERHOME/pi_temp/pi_temp.py 2>/dev/null

if [ "$?" = "0" ]; then
	echo -e  "$CYAN[+]$DEFAULT pi_temp.py made executable."
else
	echo -e  "$RED[+]$DEFAULT Failed to make pi_temp.py executable."
	SUCCESS=1
fi

# create softlink in /usr/bin/local (pi_temp OR pitemp)

LINK=/usr/local/bin/pi_temp

if [ -L $LINK ]; then
	sudo rm $LINK
fi

sudo ln -s $USERHOME/pi_temp/pi_temp.py /usr/local/bin/pi_temp 2>/dev/null

if [ "$?" = "0" ]; then
	echo -e  "$CYAN[+]$DEFAULT Create softlink pi_temp."
else
	echo -e  "$RED[+]$DEFAULT Failed to create softlink - Run install as root."
	SUCCESS=1
fi

LINK=/usr/local/bin/pitemp

if [ -L $LINK ]; then
	sudo rm $LINK
fi

sudo ln -s $USERHOME/pi_temp/pi_temp.py /usr/local/bin/pitemp 2>/dev/null

if [ "$?" = "0" ]; then
	echo -e  "$CYAN[+]$DEFAULT Created softlink pitemp."
else
	echo -e  "$RED[+]$DEFAULT Failed to create softlink - Run install as root."
	SUCCESS=1
fi

# adjust and move .service to /etc/systemd/system/

before="WorkingDirectory=/home/pi/pi_temp"
after="WorkingDirectory=${USERHOME}/pi_temp"

sed -i "s|$before|$after|g" ./files/pi_temp.service 2>/dev/null

if [ "$?" = "1" ]; then
	echo -e  "$RED[+]$DEFAULT Failed to configure service pi_temp."
	SUCCESS=1
fi

sudo cp files/pi_temp.service /etc/systemd/system/ 2>/dev/null

if [ "$?" = "0" ]; then
	echo -e  "$CYAN[+]$DEFAULT pi_temp.service created successfully."
else
	echo -e  "$RED[+]$DEFAULT Failed to create service pi_temp.  Run install as root."
	SUCCESS=1
fi

echo -e ""

