FROM ubuntu:16.04
RUN apt-get update
RUN apt-get install
RUN apt-get install sudo
RUN apt-get -y install curl
RUN apt-get -y install git
RUN apt-get -y install npm
RUN apt install -y software-properties-common
RUN  add-apt-repository ppa:gluster/glusterfs-7
RUN sudo apt-get install -y glusterfs-client
RUN apt-get -y install attr
RUN mkdir -p public/uploads
RUN curl -sL https://deb.nodesource.com/setup_12.x | sudo bash -
RUN sudo apt-get -y install nodejs
RUN sudo apt-get update
RUN git clone https://github.com/CORE-UPM/quiz_2020.git
EXPOSE 3000
EXPOSE 3006
WORKDIR /quiz_2020
CMD npm install; npm install mysql2; export DATABASE_URL= DATABASE_URL=mysql://quiz:xxxx@20.20.4.31:3306/quiz;  export QUIZ_OPEN_REGISTER=yes;  npm run-script migrate_cdps; npm run-script seed_cdps; mkdir /mnt/nas; mount -t glusterfs 20.20.4.21:/nas /mnt/nas; npm run super;
