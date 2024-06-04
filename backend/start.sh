#!/bin/bash

DEVICE_PATH="/dev/ttyUSB0"
if [ -c "$DEVICE_PATH" ]
then
    echo -e "\n\n\tDevice $DEVICE_PATH is accessible.\n\n"
else
    echo -e "\nError: Device $DEVICE_PATH is not accessible.\n\nPlease check the device path or connection.\n\nMaybe you forgot to mount the device?\n\nExample docker run command: \n\tdocker run --device=/dev/ttyUSB0:/dev/ttyUSB0 -p 5000:5000 chess-backend\n\n"
    exit 1
fi

# Start the Python application
echo -e "\n\n\tStarting Python application...\n\n"
python server.py
