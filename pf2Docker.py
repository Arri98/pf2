#!/usr/bin/python

import sys
from subprocess import call
import os


call(["sudo","docker", "build", "-t", "server", "Server/."])
call(["sudo","docker", "build", "-t", "gluster", "Gluster/."])
call(["sudo","docker", "build", "-t", "nas", "Gluster/NAS/."])
os.chdir("Compose")
call(["sudo", "docker-compose","up"])