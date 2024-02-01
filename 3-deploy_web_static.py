#!/usr/bin/python3
"""
TGZ
"""
from fabric.api import *
import os
from datetime import datetime

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
    try:
        file_name = archive_path.split("/")[-1]
        no_extension = file_name.split(".")[0]
        release_path = "/data/web_static/releases/"
        # Upload the archive to /tmp/
        put(archive_path, '/tmp/')
        # Create the release directory
        run('sudo mkdir -p {}{}/'.format(release_path, no_extension))
        # Extract the contents to the release directory
        run('sudo tar -xzf /tmp/{} -C {}{}/'.format(
            file_name, release_path, no_extension))
        # Remove the temporary archive file
        run('sudo rm /tmp/{}'.format(file_name))
        # Move contents from web_static subdirectory to release directory
        run('sudo mv {}/web_static/* {}/'.format(
            release_path + no_extension, release_path + no_extension))
        # Remove the web_static directory within the release directory
        run('sudo rm -rf {}/web_static'.format(release_path + no_extension))
        # Remove the current symbolic link
        run('sudo rm -rf /data/web_static/current')
        # Create a new symbolic link
        run('sudo ln -s {}/ /data/web_static/current'.format(
            release_path + no_extension))
        return True
    except Exception as e:
        print("Error: {}".format(str(e)))
        return False


def deploy():
    """
    deploy
    """
    path = do_pack()
    if path:
        return do_deploy(path)
    else:
        return False
