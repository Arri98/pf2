#!/usr/bin/python

import sys
from subprocess import call
import time
import os


def crear():
    os.chdir("/mnt/tmp")
    if(os.path.exists(os.getcwd()+"/pc2/")):
        print("Ya esta creado")
 	
    else:
        print("Creando")    
        os.chdir("/mnt/tmp")
        call(["wget","http://idefix.dit.upm.es/cdps/pc2/pc2.tgz"])
        call(["sudo","vnx","--unpack","pc2.tgz"])
        os.chdir(os.getcwd()+"/pc2/")
        call(["bin/prepare-pc2-labo"])

        call(["sudo","vnx", "-f", "pc2.xml", "--create"])


def arrancar():
   call(["sudo","vnx", "-f", "/mnt/tmp/pc2/pc2.xml", "--start"])


def configuracionbasededatos():

    print("Creacion  Base de Datos")
    call(["sudo", "lxc-attach", "--clear-env", "-n", "bbdd", "--", "apt", "update"])
    call(["sudo", "lxc-attach", "--clear-env", "-n", "bbdd", "--", "apt", "-y", "install", "mariadb-server"])
    call(["sudo", "lxc-attach", "--clear-env", "-n", "bbdd", "--", "sed", "-i", "-e", "s/bind-address.*/bind-address=0.0.0.0/", "-e" ,"s/utf8mb4/utf8/","/etc/mysql/mariadb.conf.d/50-server.cnf"])
    call(["sudo", "lxc-attach", "--clear-env", "-n", "bbdd", "--", "systemctl", "restart", "mysql"])
    call(["sudo", "lxc-attach", "--clear-env", "-n", "bbdd", "--", "mysqladmin", "-u", "root", "password", "xxxx"])
    print("Creando usuario")
    call(["sudo", "lxc-attach", "--clear-env", "-n", "bbdd", "--", "mysql", "-u", "root", "--password='xxxx'", "-e", "CREATE USER 'quiz' IDENTIFIED BY 'xxxx';"])
    call(["sudo", "lxc-attach", "--clear-env", "-n", "bbdd", "--", "mysql", "-u", "root", "--password='xxxx'", "-e", "CREATE DATABASE quiz;"])
    call(["sudo", "lxc-attach", "--clear-env", "-n", "bbdd", "--", "mysql", "-u", "root", "--password='xxxx'", "-e", "GRANT ALL PRIVILEGES ON quiz.* to 'quiz'@'localhost' IDENTIFIED by 'xxxx';"])
    call(["sudo", "lxc-attach", "--clear-env", "-n", "bbdd", "--", "mysql", "-u", "root", "--password='xxxx'", "-e", "GRANT ALL PRIVILEGES ON quiz.* to 'quiz'@'%' IDENTIFIED by 'xxxx';"])
    call(["sudo", "lxc-attach", "--clear-env", "-n", "bbdd", "--", "mysql", "-u", "root", "--password='xxxx'", "-e", "FLUSH PRIVILEGES;"])


def configuracioncortafuegos():
    print("Configuramos Cortafuegos")    
    comando= "scp ~/Desktop/pf2/pf2/fw.fw root@fw:/root"  
    call(comando, shell=True)	 
    comando= "sudo lxc-attach --clear-env -n fw -- bash -c  /root/fw.fw "	
    call(comando, shell=True)	


def configurarGluster():
    print("Configuramos Gluster")
    for i in range(2):    
        call(["sudo", "lxc-attach", "--clear-env", "-n", "nas"+str(i+1), "--" , "mkdir","-p", "/mnt/nas"])
    call(["sudo", "lxc-attach", "--clear-env", "-n", "bbdd", "--", "gluster", "peer", "probe", "20.20.4.21"])
    call(["sudo", "lxc-attach", "--clear-env", "-n", "bbdd", "--", "gluster", "peer", "probe", "20.20.4.22"])
    call(["sudo", "lxc-attach", "--clear-env", "-n", "bbdd", "--", "gluster", "peer", "probe", "20.20.4.23"])
    call(["sudo", "lxc-attach", "--clear-env", "-n", "bbdd", "--", "gluster", "peer", "status"])
    call(["sudo", "lxc-attach", "--clear-env", "-n", "bbdd", "--", "gluster", "volume", "create", "nas", "replica", "3", "20.20.4.21:/nas", "20.20.4.22:/nas", "20.20.4.23:/nas", "force"])
    call(["sudo", "lxc-attach", "--clear-env", "-n", "bbdd", "--", "gluster", "volume", "start", "nas"])
    print("Estado de los volumenes")
    call(["sudo", "lxc-attach", "--clear-env", "-n", "bbdd", "--", "gluster", "volume", "info"])
    call(["sudo", "lxc-attach", "--clear-env", "-n", "bbdd", "--", "gluster", "volume", "set", "nas", "network.ping-timeout", "5"])
    

def configuracionbalanceador():
    call(['sudo lxc-attach --clear-env -n lb -- sudo apt update'], shell=True)
    call(['sudo lxc-attach --clear-env -n lb -- sudo apt -y install haproxy'], shell=True)
    call(['sudo lxc-attach --clear-env -n lb -- sudo service apache2 stop'], shell=True)       
    call(['sudo lxc-attach --clear-env -n lb -- bash -c "echo \'\nfrontend lb\n\tbind *:80\n\tmode http\n\tdefault_backend webservers\n\nbackend webservers\n\tmode http\n\tbalance roundrobin\' >> /etc/haproxy/haproxy.cfg"'], shell=True)
    call(['sudo lxc-attach --clear-env -n lb -- bash -c "echo \'\tserver s1 20.20.3.11:3000 check\' >> /etc/haproxy/haproxy.cfg"'], shell=True)
    call(['sudo lxc-attach --clear-env -n lb -- bash -c "echo \'\tserver s2 20.20.3.12:3000 check\' >> /etc/haproxy/haproxy.cfg"'], shell=True)
    call(['sudo lxc-attach --clear-env -n lb -- bash -c "echo \'\tserver s3 20.20.3.13:3000 check\' >> /etc/haproxy/haproxy.cfg"'], shell=True)
 	
    call(['sudo lxc-attach --clear-env -n lb -- sudo service haproxy restart'], shell=True)  


def vamosquiz():

 for i in range(3):
     print("\n\nConfigurando: " + str(i))
     print("\n\n")
     call(["sudo", "lxc-attach","--clear-env", "-n", "s"+str(i+1), "--", "sudo", "apt-get", "update"])
     call(["sudo", "lxc-attach","--clear-env", "-n", "s"+str(i+1), "--", "curl","-sL","https://deb.nodesource.com/setup_13.x","|","sudo","-E","bash","-"],shell=True) 
     call(["sudo", "lxc-attach","--clear-env", "-n", "s"+str(i+1), "--", "sudo", "apt-get", "-y", "install", "nodejs"])
     call(["sudo", "lxc-attach", "--clear-env", "-n", "s"+str(i+1), "--", "git", "clone", "https://github.com/CORE-UPM/quiz_2020.git"])
     call(["sudo", "lxc-attach", "--clear-env", "-n", "s"+str(i+1),  "--", "add-apt-repository", "ppa:gluster/glusterfs-7"])
     call(["sudo", "lxc-attach", "--clear-env", "-n", "s"+str(i+1),  "--","apt-get", "install", "-y", "glusterfs-client"])
     call(["sudo", "lxc-attach", "--clear-env", "-n", "s"+str(i+1),  "--", "sudo", "apt-get", "install", "-y", "attr"])
     call("sudo lxc-attach -n s1 -- bash -c 'cd /quiz_2020; npm install; npm install mysql2; npm install forever;sudo mount -t glusterfs 20.20.4.21:/nas /quiz_2020/public/uploads; export CLOUDINARY_URL=public/uploads;  export QUIZ_OPEN_REGISTER=yes;export DATABASE_URL=mysql://quiz:xxxx@20.20.4.31:3306/quiz ; npm run-script migrate_cdps; npm run-script seed_cdps; ./node_modules/forever/bin/forever start ./bin/www '", shell=True)
     #call("sudo lxc-attach -n s"+str(i+1)+" -- ln -s public/uploads /mnt/nas", shell=True)	

def parar():
 os.chdir('/mnt/tmp/pc2/')
 call(["sudo", "vnx", "-f", "pc2.xml", "--shutdown"])


crear()
configuracionbasededatos()
configurarGluster()
configurarGluster()
vamosquiz()
configuracionbalanceador()
configuracioncortafuegos()



#configuracion roundrobin














