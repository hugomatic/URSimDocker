# get ip
ip=`ip addr show $(ip route | awk '/default/ { print $5 }') | grep "inet" | head -n 1 | awk '/inet/ {print $2}' | cut -d'/' -f1`
# write to file
echo "export host_ip=$ip" > host.sh
# build container
docker build -t ursim/ur10 .
