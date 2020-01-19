FROM ubuntu:16.04
RUN apt-get -y update && apt-get -y upgrade
RUN apt-get install -y --allow-unauthenticated glusterfs-server
RUN apt-get -y --allow-unauthenticated install sudo
CMD sudo service glusterfs-server start; sudo gluster peer probe 20.20.4.21; sudo gluster peer probe 20.20.4.22; sudo gluster peer probe 20.20.4.23; gluster peer status; gluster pool list; sudo gluster  volume create nas replica 3 transport tcp 20.20.4.21:/glusterbrick/brick 20.20.4.22:/glusterbrick/brick  20.20.4.23:/glusterbrick/brick  force; gluster volume start nas; gluster volume set nas network.ping-timeout 5; while true; do sleep 1000; done
EXPOSE 2222 111 245 443 24007 2049 8080 6010 6011 6012 38465 38466 38468 38469 49152 49153 49154 49156 49157 49158 4
