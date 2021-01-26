"""
    This script is for opening the ports on the infected devices.
    This script would not be installed on the server.
    
    Autheur: Jorick van Brunschot.
"""
VERSION = 1.0
defaultOpenPort = [1337,3141,7337]
defaultClosePort = [3141,7337,1337]

import argparse
import os, sys

def knock(host, ports):
    try:
        for port in ports:
            print ("knock: " + port )
        print("Penny!")
    except:
        sys.exit("Knocking error!")
    

parser = argparse.ArgumentParser()
parser.add_argument("-V", "--version", help="Show program version", action="store_true")
parser.add_argument("-O", "--open", help="Open host port", action="store_true")
parser.add_argument("-C", "--close", help="Open host port", action="store_true")
parser.add_argument("-H", "--host", help="Goal host")
parser.add_argument("-P", "--ports", help="Optional - available knocking ports. Default is for opening 1337,3141,7337 and closing 3141,7337,1337. seperated by commas without spaces.")
args = parser.parse_args()

if args.version:
    sys.exit("Version: {}".format(VERSION))

if args.open and args.close:
    sys.exit("You can only close or open. Not both.")

if !args.host:
    sys.exit("We need a host to knock.")
    
if args.open:
    if args.ports:
        defaultOpenPort = args.ports.split(",")
        
    knock(defaultOpenPort)

elif args.close:
    if args.ports:
        defaultClosePort = args.ports.split(",")
    knock(defaultClosePort)
