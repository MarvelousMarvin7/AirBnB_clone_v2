#!/usr/bin/python3
"""distributes an archive to your web servers, using the function do_deploy"""

from fabric.api import *
from fabric.operations import run, put, sudo
import os.path
env.hosts = ['3.85.196.66', '54.175.225.232']


def do_deploy(archive_path):
    """deploy acrhived .tgz to webservers"""
    if not os.path.exists(archive_path):
        return False

    try:
        # Get the filename without extension
        filename = os.path.basename(archive_path)
        file_without_ext = filename.split(".")[0]

        put(archive_path, '/tmp/')
        new_folder = ("/data/web_static/releases/{}".format(file_without_ext))
        run("sudo mkdir -p {}".format(new_folder))
        run("sudo tar -xzf /tmp/{} -C {}".format(filename, new_folder))
        run("sudo rm /tmp/{}".format(filename))
        run("sudo mv {}/web_static/* {}/".format(new_folder, new_folder))
        run("sudo rm -rf {}/web_static".format(new_folder))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {} /data/web_static/current".format(new_folder))
        return True
    except Exception as e:
        print("An error occured: {}".format(e))
        return False