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
#arrancar escenario virtual
        os.chdir("/mnt/tmp")
        call(["wget","http://idefix.dit.upm.es/cdps/pc2/pc2.tgz"])
        call(["sudo","vnx","--unpack","pc2.tgz"])
        os.chdir(os.getcwd()+"/pc2/")
        call(["bin/prepare-pc2-labo"])
#gestionar el escenario virtual
        call(["sudo","vnx", "-f", "pc2.xml", "--create"])
#call(["ssh","root@s1"])

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
    
def configurarGluster():
    print("Configuramos Gluster")
    call(["sudo", "lxc-attach", "--clear-env", "-n", "bbdd", "--", "gluster", "peer", "probe", "20.20.4.21"])
    call(["sudo", "lxc-attach", "--clear-env", "-n", "bbdd", "--", "gluster", "peer", "probe", "20.20.4.22"])
    call(["sudo", "lxc-attach", "--clear-env", "-n", "bbdd", "--", "gluster", "peer", "probe", "20.20.4.23"])
    call(["sudo", "lxc-attach", "--clear-env", "-n", "bbdd", "--", "gluster", "peer", "status"])
    call(["sudo", "lxc-attach", "--clear-env", "-n", "bbdd", "--", "gluster", "volume" "create", "nas", "replica", "3", "20.20.4.21:/nas", "20.20.4.22:/nas", "20.20.4.23_/nas", "force"])
    call(["sudo", "lxc-attach", "--clear-env", "-n", "bbdd", "--", "gluster", "volume", "start", "nas"])
    print("Estado de los volumenes")
    call(["sudo", "lxc-attach", "--clear-env", "-n", "bbdd", "--", "gluster", "volume", "info"])
    call(["sudo", "lxc-attach", "--clear-env", "-n", "bbdd", "--",  "set", "nas", "network.ping-timeout", "5"])

    
    for i in range(2):    
        call(["sudo", "lxc-attach", "--clear-env", "-n", "nas"+i+1, "--" , "mkdir", "/mnt/nas"])
        call(["sudo", "lxc-attach", "--clear-env", "-n", "nas"+i+1,"mount","-t","glusterfs", "20.20.4.2"+str(i+1)+":/nas", "mnt/nas"])


    
def configuracionbalanceador():

    call(["sudo", "lxc-attach", "--clear-env", "-n", "bbdd", "--" "bash -c" ,"echo \'\ s1 20.20.3.11:80 check\' >> /etc/haproxy//haproxy.cfg'", "shell=True"])
    call(["sudo", "lxc-attach", "--clear-env", "-n", "bbdd", "--" "bash" ,"-c", "echo \'\ s2 20.20.3.12:80 check\' >> /etc/haproxy//haproxy.cfg'", "shell=True"])
    call(["sudo", "lxc-attach", "--clear-env", "-n", "bbdd", "--" "bash" ,"-c", "echo \'\ s3 20.20.3.13:80 check\' >> /etc/haproxy//haproxy.cfg'", "shell=True"])
    call(["sudo", "lxc-attach", "--clear-env", "-n", "bbdd", "--" "bash", "-c", "echo \'\nfrontend lb\n\tbind ]:80\n\tmode http\n\tdefault_backend webservers\n\backend webservers\n\tmode http\n\tbalance roundrobin\' >> /etc/haproxy//haproxy.cfg'", "shell=True"])

def crearLB():


#modificar imagen de maquinas virtuales


#    call(["sudo","vnx","-f","pc2.xml","--destroy"])
    call(["sudo","vnx","--modify-rootfs","filesystems/rootfs_lxc64-cdps","--arch=x86_64"])
    call(["sudo","dhclient","eth0"])
    call(["cd","pc2"])
    call(["bin/prepare-pc2-labo"])



#para conservando cambios call(["sudo", "vnx", "-f", "pc2.xml", "--shutdown"])
#rearranca el escenario anterior call(["sudo", "vnx", "-f", "pc2.xml", "--start"])
#para borrando los cambios call(["sudo", "vnx", "-f", "pc2.xml", "--destroy"])
#parar y rearrcancar individualmente call(["sudo", "vnx", "-f", "pc2.xml", "--shutdown", "-M", "fw"])
#mostrar mapa del escenario call(["sudo","vnx", "-f", "pc2.xml", "--show-map"])


def vamosquiz():


 call(["sudo", "lxc-attach", "-n", "s"+str(i+1), "--", "sudo", "apt-get", "update"])
 call(["sudo", "lxc-attach", "-n", "s"+str(i+1), "--", "sudo", "apt-get", "-y", "install", "nodejs"])
 call(["sudo", "lxc-attach", "-n", "s"+str(i+1), "--", "sudo", "apt-get", "-y" ,"install", "npm"])
 call(["sudo", "lxc-attach", "-n", "s"+str(i+1), "--" ,"sudo" ,"nodejs", "-v"])
 
 call(["sudo", "lxc-attach", "-n" ,"s1", "--", "sudo", "-c", "./node_modules/forever/bin/forever", "start", "./bin/www "])
for i in range(2):
 call(["sudo", "lxc-attach", "--clear-env", "-n", "s"+str(i+1), "--", "sudo", "git", "clone", "https://github.com/CORE-UPM/quiz_2020.git"])
 call(["sudo", "lxc-attach", "--clear-env", "-n", "s"+str(i+1),  "--", "sudo", "cd", "/quiz_2020"])
 call(["sudo", "lxc-attach", "--clear-env", "-n", "s"+str(i+1),  "--", "sudo", "mkdir", "-p", "public/uploads"])
 call(["sudo", "lxc-attach", "--clear-env", "-n", "s"+str(i+1),  "--", "sudo", "npm", "install"])
 call(["sudo", "lxc-attach", "--clear-env", "-n", "s"+str(i+1),  "--", "sudp", "npm", "install", "forever"])
 call(["sudo", "lxc-attach", "--clear-env", "-n", "s"+str(i+1),  "--", "sudp", "npm", "install", "mysql2"])
 call(["sudo", "lxc-attach", "--clear-env", "-n", "s"+str(i+1),  "--", "sudp", "add-apt-repository", "ppa:gluster/glusterfs-7"])
 call(["sudo", "lxc-attach", "--clear-env", "-n", "s"+str(i+1),  "--", "sudp", "apt-get", "install", "-y", "glusterfs-client"])
 call(["sudo", "lxc-attach", "--clear-env", "-n", "s"+str(i+1),  "--", "sudp", "apt-get", "install", "-y", "attr"])
 call(["sudo", "lxc-attach", "--clear-env", "-n", "s"+str(i+1),  "--", "sudp", "export", "QUIZ_OPEN_REGISTER=yes"])
 call(["sudo", "lxc-attach", "--clear-env", "-n", "s"+str(i+1),  "--", "sudp", "export", "CLOUDINARY_URL=public/uploads"])
 call(["sudo", "lxc-attach", "--clear-env", "-n", "s"+str(i+1), "--", "sudp", "-c", "DATABASE_URL=mysql://quiz:xxxx@20.20.4.31:3306/quiz"])
 call(["sudo", "lxc-attach", "--clear-env", "-n", "s"+str(i+1), "--" , "mkdir", "/mnt/nas"])
 call(["sudo", "lxc-attach", "--clear-env", "-n", "s"+str(i+1),"mount","-t","glusterfs", "20.20.4.2"+str(i+1)+":/nas", "mnt/nas"])
 if i=0:
    call(["sudo", "lxc-attach", "--clear-env", "-n",  "s1", "--", "sudo", "npm", "run-script", "migrate_cdps"])
    call(["sudo", "lxc-attach", "--clear-env", "-n",  "s1", "--", "sudo", "npm", "run-script", "seed_cdps"])
   


vamosquiz()
'''
def definirproxy():
 call("sudo lxc-attach --clear-env -n "s"+str(i), " "--", "sudo", "service", "haproxy", "restart")

def rearrancarHAproxy():
 call("sudo lxc-attach --clear-env -n "s"+str(i), " "--", "sudo", "service", "haproxy", "restart")

#call(["ssh","root@s1"])
'''

#configuracion roundrobin











