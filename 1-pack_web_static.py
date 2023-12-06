#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents of the
web_static folder of your AirBnB Clone repo, using the function do_pack
"""


from datetime import datetime
from fabric.operations import local


def do_pack():
    """ compress files"""
    local("mkdir -p versions")
    result = ("tar -cvzf versions/web_static_{}.tgz web_static"
              .format(datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")),
              capture=False)
    if result.succeeded:
        return result
    return None
