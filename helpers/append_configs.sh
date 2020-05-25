sudo wg-quick down hs3wg
sudo cat ../configs_to_append.txt >> /etc/wireguard/hs3wg
sudo wg-quick up hs3wg
rm ../configs_to_append.txt
