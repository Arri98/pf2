FROM ubuntu:16.04
RUN apt-get -y update && apt-get -y upgrade
RUN apt-get install -y --allow-unauthenticated glusterfs-server
RUN apt-get -y --allow-unauthenticated install sudo
CMD sudo service glusterfs-server start; sudo gluster peer probe 20.20.4.21; sudo gluster peer probe 20.20.4.22; sudo gluster peer probe 20.20.4.23; sudo gluster  volume create nas replica 2 transport tcp 20.20.4.21:/exp1 20.20.4.22:/exp2 20.20.4.23:/exp3 force; gluster volume start nas; gluster volume set nas network.ping-timeout 5
EXPOSE 2222 111 245 443 24007 2049 8080 6010 6011 6012 38465 38466 38468 38469 49152 49153 49154 49156 49157 49158 49159 49160 49161 49162
