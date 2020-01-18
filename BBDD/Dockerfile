FROM ubuntu:16.04
RUN apt update
RUN apt -y install mariadb-server
RUN sed -i -e s/bind-address.*/bind-address=0.0.0.0/ -e s/utf8mb4/utf8/ /etc/mysql/mariadb.conf.d/50-server.cnf
RUN systemctl restart mysql
RUN mysqladmin -u root password xxxx
RUN mysql -u root --password='xxxx' -e "CREATE USER 'quiz' IDENTIFIED BY 'xxxx';"
RUN mysql -u root --password='xxxx' -e "CREATE DATABASE quiz;
RUN mysql -u root --password='xxxx' -e "GRANT ALL PRIVILEGES ON quiz.* to 'quiz'@'localhost' IDENTIFIED by 'xxxx';
RUN ysql -u root --password='xxxx' -e "GRANT ALL PRIVILEGES ON quiz.* to 'quiz'@'%' IDENTIFIED by 'xxxx';"
RUN mysql -u root --password='xxxx' -e "FLUSH PRIVILEGES;"
EXPOSE 3000
