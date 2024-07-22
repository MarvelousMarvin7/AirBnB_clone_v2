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
    if not os.path.exists(archive_path):
        return False

    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, no_ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext))
        run('rm /tmp/{}'.format(file_n))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        run('rm -rf {}{}/web_static'.format(path, no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
        return True
    except:
        return False


def deploy():
    """deploy fully"""
    try:
        path = do_pack()

        if path is None:
            return False

        return do_deploy(path)
    except Exception as e:
        print("An error occured durring deploying process: {}".format(e))
        return False
