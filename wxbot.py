#!/usr/bin/env python3
# Alert bot, based on Webex API
# author: Carmelo C
# email: carmelo.califano@gmail.com
# history, date format ISO 8601:
#  2024-10-01  1.0 Initial version

# Import some modules
import json           # JSON encoder and decoder
import logging        # Logging facility for Python
import os             # Miscellaneous operating system interfaces
import re             # Regular expression operations
import requests       # Python HTTP for Humans
import subprocess     # Subprocess management
import time           # Time access and conversions

# General settings
# source: https://developer.webex.com/docs/bots
BASEURL = 'https://webexapis.com/v1/messages'
LOGFILE = '/var/log/auth.log'

# Version info
__version__ = "1.0"
__build__ = "20241001"


def readConf():
    """ 
    read_conf() reads the application's configuration from an external file.
    The file is JSON-formatted and contains:
      the token,
      the room ID.
    """
    with open('wxbot.json', 'r') as config_in:
        config_json = json.load(config_in)
    return config_json


def wxSend(message, token, roomid):
    """
    wxSend() consumes Webex API messages endpoint to publish a message on the room.
    Required arguments are:
      the token,
      the chat ID.
    """
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    payload = {
        'roomId': roomid,
        'markdown': message
    }
    url = BASEURL
    response = requests.post(url = url, headers = headers, json = payload)


def countLines(string):
    return len(string.splitlines())


def groupIPs(string):
    match1 = re.findall(r'from\b.+\bport', string.decode('utf-8'))
    match2 = [m.lstrip('from ').rstrip(' port') for m in match1]
    res = {}
    for ip_addr in match2:
        res[ip_addr] = match2.count(ip_addr)
    return res

def main():
    # Initialization, wxbot.log shall be stored in the same directory
    logging.basicConfig(filename = 'wxbot.log', level = logging.INFO)

    LASTHOUR = time.asctime()[4:13]  # E.g.: 'Jun  5 11'
    BADGUY = 'Invalid'
    config = readConf()
    bearer = config['BEARER']
    roomid = config['ROOM_ID']
    count = 0
    msg2 = ' access attempts in the last hour'

    try:
        # Parses LOGFILE within LASTHOUR, sends to PIPE
        filtered_auth_temp = subprocess.Popen(['grep', LASTHOUR, LOGFILE], stdout = subprocess.PIPE)
        # Reads from PIPE to search for BADGUY
        filtered_auth = subprocess.check_output(['grep', BADGUY], stdin = filtered_auth_temp.stdout)

        # Eventually, we'll get an output that only shows the interesting lines:
        # b'<timestamp> <hostname> sshd[12786]: Invalid user <attacker> from <ip_address> port <port_number>\n ..."
        # the type will be 'bytes'

        # Finally the output will be split based on newline ('\n') characters
        count = countLines(filtered_auth)
        ip_list = groupIPs(filtered_auth)
    except:
        pass

    if count:
        logging.info(f'[!] {os.path.basename(__file__)}: {count} unauthorized' + msg2)
        msg1 = str(count) + ' unauthorized'
        wxSend(msg1 + msg2, bearer, roomid)
        wxSend(str(ip_list), bearer, roomid)
    else:
        logging.info(f'[+] {os.path.basename(__file__)}: No' + msg2)


# Main function
if __name__ == '__main__':
    main()

