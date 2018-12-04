elasticsearch         6.5.1                     
elasticsearch-curator 5.5.4-1                    
kibana                6.5.1
logstash              6.5.1

#Rsyslog 8.39 compiled with redis support on Centos 7.5

yum install -y gcc libestr-devel libfastjson4-devel zlib-devel libuuid-devel libgcrypt-devel libcurl-devel systemd-devel hiredis-devel
wget http://www.rsyslog.com/files/download/rsyslog/rsyslog-8.39.0.tar.gz
tar -zxvf rsyslog-8.39.0.tar.gz
cd rsyslog-8.39.0
./configure --enable-omhiredis --enable-imjournal
./make
./make install

#/var/log/raw and /var/log/processed are symlinks to zfs partition with lz4 compression.
https://linuxhint.com/install-zfs-centos7/
zfs set compression=lz4 zfspoolname
