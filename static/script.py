#!/bin/python

from shutil import which
import sys, os  
import re, requests
import json
import argparse

client_conf_template = \
'''
[Interface]
Address = {ip_address}/32
PrivateKey = {client_privkey}

[Peer]
PublicKey = {server_pubkey}
AllowedIPs = {allowed_ips}
Endpoint = {endpoint}
PersistentKeepalive = 21
'''

parser = argparse.ArgumentParser(description='Wireguy\'s frontend config generator.')
parser.add_argument('--api_endpoint', type=str,
                    help='endpoint for the wireguy\'s api')
#TODO remove this option after adding keyfile and manual username/password prompt
parser.add_argument('--api_credentials_hack', type=str,
        help='plaintext username:password, to be removed later')
#TODO - in the future, one will be able to authenticate with generated keyfile - JSON with
#endpoint info, and probably some key expiring after 24h. For now MVP will use username/password
#parser.add_argument('keyfile', type=str,
#                    help='provide name of a file with config')

args = parser.parse_args()

api_endpoint = args.api_endpoint
api_credentials = tuple(args.api_credentials_hack.split(":"))


if not which("wg"):
    raise RuntimeError("wireguard is not installed(?) wg command not found.")

print("\n*** Welcome to wireguy's frontend config generator ***\n\n"
      "This script will call back to the mothership\n"
      "so that you can get server's config/pubkey and\n"
      "then your config/pubkey are automatically uploaded.")

try:
    nickname = re.sub(
        '[^0-9a-zA-Z,.?!-_żźćńółęąśŻŹĆĄŚĘŁÓŃ ]+',
        '',
        sys.argv[1]
    )
    if nickname != sys.argv[1]:
        print(f"Warning - your nickname has been sanitized to: {nickname}")
except IndexError:
    print("Error - no nickname has been provided - provide it as the script's 1st argument.")
    quit()

print("Asking mothership for wireguard access info...")
request_get_config = requests.get(
        api_endpoint + "get_config?dev_type=" + "0",
        auth=api_credentials
        )

if (request_get_config.status_code != 200):
    print(f"API request returned code: {request_get_config.status_code}. Exiting")
    quit()

config = json.loads(request_get_config.text)

print("gotten config! :\n" + str(config))

print("Generating client's keys using shell wireguard utilities")
client_privkey = os.popen("wg genkey").read()[:-1]
client_pubkey = os.popen("echo '{s}' | wg pubkey".format(s=client_privkey)).read()[:-1]


client_conf_final = client_conf_template.format(
    nickname = nickname,
    ip_address = config['client']['ip_address'],
    allowed_ips = config['client']['allowed_ips'],
    client_privkey = client_privkey,
    server_pubkey = config['server']['pubkey'],
    endpoint = config['server']['addr'] + ":" + config['server']['port']
)

request_put_config = requests.post(
        api_endpoint + "put_config",
        json = {
            'nickname': nickname,
            'client_pubkey' : client_pubkey,
            'client_ip' : config['client']['ip_address']},
        auth=api_credentials
        )

if (request_put_config.status_code != 200):
    print(f"API request returned code: {request_put_config.status_code}. Exiting")
    quit()

with open(config['wgnet_name'] + ".conf", 'w') as f: 
    f.write(client_conf_final)

