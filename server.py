from flask import Flask, send_from_directory, request
import json
from random import randint

app = Flask(__name__, static_url_path='')

server_conf_template = \
'''## {username}:
[Peer]
PublicKey = {client_pubkey}
AllowedIPs = {client_ip}/32
'''

try:
    with open('private/wireguard_config.json','r') as file:
        wg_config = json.load(file)    
except FileNotFoundError:
    print("No configuration file provided. Exiting.")
    quit()

def get_client_ip():
    #naive DHCP, like very naive. TODO FIX LOL
    return str(randint(100,250)) + "." + str(randint(1,255))

def wireguard_add_new_client(client_name, client_pubkey, client_ip):
    
    client_config = server_conf_template.format(
            username = client_name,
            client_pubkey = client_pubkey,
            client_ip = client_ip
    )
    
    print("adding client config:\n"
            f"{client_config}")

    with open("private/configs_to_append.txt", "a") as myfile:
        myfile.write(client_config +"\n\n")

@app.route('/api/get_config')
def api_get_config():
    client_data = {
            "wgnet_name": wg_config['wgnet_name'],
            "client":{         
                "ip_address":get_client_ip(),
                "allowed_ips": wg_config['allowed_ips'] 
            },
            "server":{
                "pubkey" : wg_config['public_key'],
                "addr" : wg_config['addr'],
                "port" : wg_config['port']
            }
        }

    return json.dumps(client_data)


@app.route('/api/put_config',methods = ['POST'])
def api_put_config():
    client_config = request.json
    print(client_config)
    wireguard_add_new_client(
            client_name = client_config['nickname'],
            client_pubkey = client_config['client_pubkey'],
            client_ip = client_config['client_ip']
    )
    return "OK"

@app.route('/<path:path>')
def hello_world(path):
    return send_from_directory('static',path)

@app.route('/')
def return_index():
    return send_from_directory('static',"index.html")
