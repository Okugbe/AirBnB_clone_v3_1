#!/usr/bin/python3
"""This is  script (based on the file 1-pack_web_static.py) that
distributes an archive to your web servers, using the function do_deploy"""


from fabric.api import env, put, run
from os.path import exists
import shlex
env.hosts = ['52.91.133.176', '35.175.129.100']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """All remote commands must be executed on your both web servers
    (using env.hosts = ['<IP web-01>', 'IP web-02'] variable in your script)"""
    if not exists(archive_path):
        return False
    try:
        path_name = archive_path.replace('/', ' ')
        path_name = shlex.split(path_name)
        path_name = path_name[-1]

        wname = path_name.replace('.', ' ')
        wname = shlex.split(wname)
        wname = wname[0]

        releases_path = f"/data/web_static/releases/{wname}/"
        tmp_path = f"/tmp/{pname}"

        put(archive_path, "/tmp/")
        run(f"mkdir -p {releases_path}")
        run(f"tar -xzf {tmp_path} -C {releases_path}")
        run(f"rm {tmp_path}")
        run(f"mv {releases_path}web_static/* {releases_path}")
        run(f"rm -rf {releases_path}web_static")
        run('rm -rf /data/web_static/current')
        run(f"ln -s {releases_path} /data/web_static/current")
        print("New version deployed!")
        return True
    except BaseException:
        return False
    
