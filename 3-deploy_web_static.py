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
    if not exists(archive_path):
        return False

    try:
        put(archive_path, '/tmp/')

        filename = archive_path.split('/')[-1]
        foldername = filename.split('.')[0]

        run('sudo mkdir -p /data/web_static/releases/{}/'.format(foldername))
        run('sudo tar -xzf /tmp/{} -C /data/web_static/releases/{}/'.
            format(filename, foldername))

        run('sudo rm /tmp/{}'.format(filename))

        run('sudo mv /data/web_static/releases/{}/web_static/* '
            '/data/web_static/releases/{}/'.
            format(foldername, foldername))

        run('sudo rm -rf /data/web_static/current')

        run('sudo ln -s /data/web_static/releases/{}/ /data/web_static/current'.
            format(foldername))

        print('New version deployed!')
        return True

    except:
        return False

def deploy():
    """Create and distribute an archive to a web server."""
    file = do_pack()
    if file is None:
        return False
    return do_deploy(file)
