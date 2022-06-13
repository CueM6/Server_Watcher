#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 19:57:17 2022

@author: Noble Wilson

For demo at LifeTrends interview

I didn't steal this code, I made this from scratch

Before deployment, run
$ python -m smtpd -c DebuggingServer -n localhost:1025
"""

import socket
import ssl
import subprocess
import sys
import time
import smtplib

# This won't find anything, a local mailserver needs to be set up first
from email.mime.text import MIMEText

# boring UI stuff
print("Welcome to the server health monitor")
print("PLEASE NOTE: Only works with HTTPS and SSL")
print("Enter the host IP address or domain:")
host = input()
port = 443

# Checks if host is real and working
try: 
    ssl.wrap_socket(socket.create_connection((host, port), timeout=5))
    print("Host accepted connection")
except socket.timeout:
    print("Host timed out")
    sys.exit()
except (ConnectionRefusedError, ConnectionResetError):
    print("Connection was refused by host")
    sys.exit()
except:
    print("How? Is this a real host?")
    sys.exit()
    
# Crafts packets to send to host
def ping():
    command = ["ping", "-c", "1", "-w2", host]
    return subprocess.run(args=command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0
cont = True

# Loops until host dies
while cont == True:
    if ping() == True:
        print(time.strftime('%X, %x'), ": Host is up")
        time.sleep(10)
        cont = True
    else:
        print("HOST IS DOWN")
        cont = False
        alert = True

""" This section needs your actual credentials,
since this is just a demonstration of my skills,
it wont actually send any emails """

if alert == True:
    sender = "servercheck@exampledomain.net"
    receiver = ["alertsystem@exampledomain.net"]
    mport = 1025
    mmsg = MIMEText("AHHHH WE HAVE A PROBLEM")
    mmsg['Subject'] = "Server Down"
    mmsg['From'] = "servercheck@exampledomain.net"
    mmsg['To'] = "alertsystem@exampledomain.net"

# Uncomment to actually login and send mail
#    with smtplib.SMTP('localhost', mport) as server:
#        server.login('username', 'password')
#        server.sendmail(sender, receiver, mmsg.as_string())