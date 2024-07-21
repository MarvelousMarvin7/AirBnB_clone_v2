#!/usr/bin/python3
""" Fabric script  that creates and distributes an archive to your web servers,
 using the function deploy:
"""

from fabric.api import *
from fabric.operations import local, run, put, sudo
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
    if not os.path.exists(archive_path):
        return False

    try:
        # Get the filename without extension
        filename = archive_path.split("/")[-1]
        file_without_ext = filename.split('.')[0]

        put(archive_path, '/tmp/')
        new_folder = ("/data/web_static/releases/ + {}".format(file_without_ext))
        run("sudo mkdir -p {}".format(new_folder))
        run("sudo tar -xzf /tmp/{} -C {}".format(filename, new_folder))
        run("sudo rm /tmp/{}".format(filename))
        run("sudo mv {}/web_static/* {}/".format(new_folder, new_folder))
        run("sudo rm -rf {}/web_static".format(new_folder))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {} /data/web_static/current".format(new_folder))
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
