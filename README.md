# Wireguy - simple wireguard infrastructure manager

Wireguard VPN may be the easiest way to provide access to linux-based infrastructure hidden behind NAT-ted networks.

I've created this simple tool, to automate the config generation process, and allow end users to generate private key client-side.

I'm gonna keep on improving it in my free time - while super-insecure in it's current state, it already makes my job a lot easier.

If you want to read below, you should be somehow familiar with wireguard concept - I recommend this guide: https://www.ckn.io/blog/2017/11/14/wireguard-vpn-typical-setup/

### Use cases

#### 1. Let's imagine you have:
* a bunch of raspberry-pi's at your home
* a linux-based multimedia server 
* your notebook
* a raspberry pi hidden inside wallplug at a local McDonald's
* a VPS with public IP

After setting up the wireguard server on your VPS, and then installing wireguy there, it takes less than 5 min. to add each of the aforementioned devices to the network.

#### 2. You're deploying a network for a team:

You give each member a "one-liner" bash script. Now all they have to do is:
* Install wireguard (with their package manager probably)
* Execute the "one-liner"
* `sudo mv` the generated config to the /etc/wireguard/. location
* `wg-quick up` the network

### How to client

You should execute an one-liner which will download and execute python script, leaving you with complete client config file.

`python -c "$(curl http://vpn.example.com/script.py)" --api_endpoint http://vpn.example.com/api/ --api_credentials_hack username:password`

or (to be implemented)

`python -c "$(curl http://vpn.example.com/script.py)" --api_endpoint http://vpn.example.com/api/ --api_token VGhlIGdhbWU=`

You can also download the script, and read it before executing, to make sure no monkey buisness is happening in it.

### How to server

1. Configure password acces for the API! This may be achieved using a proper nginx config - example:
```
server {
  server_name <VPN_SERVICE_DOMAIN>;
  location /api/ {
    proxy_pass http://localhost:33355; 
    auth_basic "Access restricted";
    auth_basic_user_file /etc/nginx/.htpasswd;
  }
  location / {
    proxy_pass http://localhost:33355; 
  }
```

2. Populate `private/wireguard_config.json`:

```
{
  "wgnet_name":"<any name>",
  "allowed_ips" : "Ip range of the network, eg. 10.69.0.0/16",
  "public_key" : "<wireguard server's public key>",
  "addr" : "<wireguard's endpoint>",
  "port" : "<wireguard's port>"
}
```

3. run `run.sh`

4. When a client will (succesfully) excute his script, a new entry will appear on your server, in `private/configs_to_append.txt`. Now you can append it manually to your server config.


### Project roadmap

* Allow adding config via token with expiration date. Leave interactive login-based authentication as an alternative.
* Allow automatic client adding and network restarting
* Allow client adding without restart
* Add simple database for managed clients
* Add better, role-based IP assignment (roles like `infrastructure`, `notebook`, `embedded`)
* Add browser-based frontend
* Dockerize this thing, add autobuilds, add static `tests: passing` sticker
