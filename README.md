# network_Reconnaissance


Install software:
- Python versie 3.9.0
- Nmap versie 7.91
- Knockd versie 0.7-1

Python modules:
- pip3 install netifaces
- pip3 install requests


Cronjob added:

0 1 * * * python3 scriptpath >/dev/null 2>&1

This cron job is started every day at 1 AM and doesn't generate a output file.
