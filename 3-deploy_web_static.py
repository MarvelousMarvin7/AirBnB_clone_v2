#!/usr/bin/python3
""" Fabric script  that creates and distributes an archive to your web servers,
 using the function deploy:
"""

from fabric.api import *
from fabric.operations import env, run, put
import os.path
import time
env.hosts = ['3.85.196.66', '54.175.225.232']


def do_pack():
    """generates a .tgz archive"""
    timeset = time.strftime("%Y%m%d%H%M%S")
    try:
        local("mkdir -p versions")
        local("tar -cvzf versions/web_static_{}.tgz web_static/".
              format(timeset))
        return ("versions/web_static_{}.tgz".format(timeset))
    except:
        return None


def do_deploy(archive_path):
    """deploy acrhived .tgz to webservers"""
    if (os.path.isfile(archive_path) is False):
        return False

    try:
        # Get the filename without extension
        filename = archive_path.split("/")[-1]
        new_folder = ("/data/web_static/releases/" + filename.split(".")[0])
        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(new_folder))
        run("tar -xzf /tmp/{} -C {}".format(filename, new_folder))
        run("rm /tmp/{}".format(filename))
        run("mv {}/web_static/* {}/".format(new_folder, new_folder))
        run("rm -rf {}/web_static".format(new_folder))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(new_folder))
        return True
    except:
        return False


def deploy():
    """deploy fully"""
    try:
        path = do_pack()
        return do_deploy(path)
    except Exception as e:
        print("An error occured durring deploying process: {}".format(e))
        return False
