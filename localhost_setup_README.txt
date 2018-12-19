Ind I Windows/system32/drivers/etc/hosts

127.65.43.21 frontend.leaguedraft.gg
127.65.43.22 backend.leaguedraft.gg



Skriv i cmd
netsh interface portproxy add v4tov4 listenport=80 listenaddress=127.65.43.22 connectport=5000 connectaddress=127.0.0.1
netsh interface portproxy add v4tov4 listenport=80 listenaddress=127.65.43.21 connectport=8080 connectaddress=127.0.0.1
