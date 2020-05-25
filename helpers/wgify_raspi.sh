sudo apt-get update
sudo apt-get upgrade 
sudo apt-get install -y raspberrypi-kernel-headers
echo "deb http://deb.debian.org/debian/ unstable main" | sudo tee --append /etc/apt/sources.list.d/unstable.list
sudo apt-get install -y dirmngr 
wget -O - https://ftp-master.debian.org/keys/archive-key-$(lsb_release -sr).asc | sudo apt-key add -
printf 'Package: *\nPin: release a=unstable\nPin-Priority: 150\n' | sudo tee --append /etc/apt/preferences.d/limit-unstable
sudo apt-get update
sudo apt-get install -y wireguard 

echo "TODO complete this script without compromising my private config"
#python -c "$(curl http://<ADDR>/script.py)" --api_endpoint http://<ADDR>/api/ --api_credentials_hack USER:PASS

