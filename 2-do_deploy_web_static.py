#!/usr/bin/python3
"""

"""
from fabric.api import *
import os

env.hosts = ['100.25.203.135', '100.25.46.169']


def do_pack():
    """
    Return TGZ or none
    """
    now = datetime.now()
    time_string = now.strftime("%Y%m%d%H%M%S")
    archive_name = "web_static_{}.tgz".format(time_string)
    local("sudo mkdir -p versions")
    archive_path = "versions/{}".format(archive_name)
    command = "sudo tar -czvf {} web_static".format(archive_path)
    result = local(command)
    if result.failed:
        return None
    return archive_path


def do_deploy(archive_path):
    """distributing archives to the web servers"""
    if not os.path.exists(archive_path):
        return False
    if os.path.isfile(archive_path) is False:
        return False
    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    if put(archive_path, "/tmp/{}".format(file)).failed is True:
        return False
    if run("sudo rm -rf /data/web_static/releases/{}/".
           format(name)).failed is True:
        return False
    if run("sudo mkdir -p /data/web_static/releases/{}/".
           format(name)).failed is True:
        return False
    if run("sudo tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
           format(file, name)).failed is True:
        return False
    if run("sudo rm /tmp/{}".format(file)).failed is True:
        return False
    if run("sudo mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/".format(name, name)).failed is True:
        return False
    if run("sudo rm -rf /data/web_static/releases/{}/web_static".
           format(name)).failed is True:
        return False
    if run("sudo rm -rf /data/web_static/current").failed is True:
        return False
    if run("sudo ln -s /data/web_static/releases/{}/ /data/web_static/current".
           format(name)).failed is True:
        return False
    return True
