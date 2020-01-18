FROM ubuntu:16.04
RUN apt-get update
RUN apt-get install
RUN apt-get install sudo
RUN apt-get -y install curl
RUN apt-get -y install git
RUN apt-get -y install 
RUN curl -sL https://deb.nodesource.com/setup_12.x | sudo bash -
RUN sudo apt-get -y install nodejs
RUN sudo apt-get update
RUN git clone https://github.com/CORE-UPM/quiz_2020.git
EXPOSE 3000
EXPOSE 3006
WORKDIR /quiz_2020
CMD npm install; npm install forever; npm install mysql2; npm run-script migrate_local; export QUIZ_OPEN_REGISTER=yes; export DATABASE_URL= DATABASE_URL=mysql://quiz:xxxx@20.20.4.31:3306/quiz;  npm run-script seed_local; ./node_modules/forever/bin/forever start ./bin/www;