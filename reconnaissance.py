# Version:      0.1  
# Autheur:      Jorick van Brunschot (jorick.van.brunschot@hva.nl) 500838348
# datum:        
#
# todo:
# 
# get hostname from device and put it into list (nice to have)
# start scanNetworkPorts with multithreading (https://docs.python.org/3/library/threading.html)

import os
import subprocess
import re
import netifaces as ni
import ipaddress
import requests
import json
from datetime import datetime

def uploadToPastebin(title: str, text: str):
    #uploads it to pastebin. 
    #returns just the statuscode of the paste. If needed in future it can return the url or more.
    #now api username and password plain text (of test account) 
    PASTEFORMAT = "json"
    KEY = PASTEBINAPIKEY

    login_data = {
        'api_dev_key': KEY,
        'api_user_name': USERNAME,
        'api_user_password': PASSWORD
        }
    data = {
        'api_option': 'paste',
        'api_dev_key':KEY,
        'api_paste_code':text,
        'api_paste_private': '2',
        'api_paste_name':title,
        'api_paste_expire_date': '1M',
        'api_user_key': None,
        'api_paste_format': PASTEFORMAT
        }
    
    login = requests.post("https://pastebin.com/api/api_login.php", data=login_data)
    #status code for the logging is showed by: login.status_code (needs to be 200)
 
    data['api_user_key'] = login.text
    postToPastebin = requests.post("https://pastebin.com/api/api_post.php", data=data)
    #URL is able to show with: postToPastebin.text
    return(postToPastebin.status_code)

def scanNetworkPorts(ipadress: str, netMask: int):
    #scan's the network for open devices. 
    #each open device it retrieves the open ports
    #Returns a list of dict's with ip and a list with open ports
    #
    #ToDo:
    
    netIp = str(ipaddress.ip_network("{}/{}".format(ipadress,netMask), strict=False))

    outputFile = "nmap-output_" + netIp.replace(".","-").replace("/","_")
    command = "nmap -sS -oG {} {}".format(outputFile, netIp)

    #test = subprocess.Popen(command, stdout=subprocess.PIPE).stdout.read()
    openHosts = []
    with open(outputFile, "r") as nmapOutput:
        for line in nmapOutput:
            if line[0:4] != "Host":
                continue
            ip = re.findall(r'(?:\d{1,3}\.)+(?:\d{1,3})',line)[0]

            openPorts = ""
            if "Ports:" in line:
                openPorts = re.findall(r'(?:\d{1,5})',line.split("Ports: ")[1])
            
            if len(openHosts) == 0:
                 openHosts.append({"ip":ip, "openports": openPorts})
            else:
                hostExists = None
                for host in range(len(openHosts)):
                    if openHosts[host]["ip"] == ip:
                        hostExists = host
                        break
                
                if hostExists == None :
                    openHosts.append({"ip":ip , "openports":openPorts })
                elif openHosts[hostExists]["openports"] == "":
                    openHosts[hostExists]["openports"] = openPorts
                else:
                    openHosts[hostExists]["openports"].append(openPorts)
    return openHosts

def getInterfaceAdresses():
    #Check all local network interfaces 
    #ipv4 only support
    #ipv6 isnt implemented (yet)
    #returns list of dicts 
    interfaceIpAdresses = []
    LOCALHOST = '127.0.0.1'
    for interface in ni.interfaces():
        try:
            assert ni.ifaddresses(interface)[ni.AF_INET]     
        except:
            continue

        for network in ni.ifaddresses(interface)[ni.AF_INET]:
            if LOCALHOST == network['addr']:
                continue
            network["netmask"] = ipaddress.IPv4Network("0.0.0.0/" + network["netmask"]).prefixlen
            interfaceIpAdresses.append(network)
    return interfaceIpAdresses

if __name__ == '__main__':
    wanIP = requests.get("https://api.ipify.org").text
    networkDetails = {
        "wanip": wanIP,
        "date": datetime.now().strftime("%d-%m-%Y"),
        "interfaces" : []
    }
    for network in getInterfaceAdresses():
        interfaceIP = network['addr']
        interfaceNetmask = network['netmask']
        interfaceOpenDevices = scanNetworkPorts(interfaceIP,interfaceNetmask)
        networkDetails["interfaces"].append({"ip":interfaceIP, "netmask":interfaceNetmask, "networkdevices":interfaceOpenDevices})
    uploadToPastebin(wanIP + "_output",json.dumps(networkDetails))
