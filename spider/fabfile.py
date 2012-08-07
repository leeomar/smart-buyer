#!/bin/python
from fabric.api import local, settings, abort, run, cd
from fabric.api import task
from fabric.api import env
from fabric.contrib.console import confirm
import install

env.hosts = ['127.0.0.1', ]
#env.user = ""
#env.password = ""

'''
@task
def test():
    with settings(warn_only=True):
        result = local('./manage.py test my_app', capture=True)
    if result.failed and not confirm("Tests failed. Continue anyway?"):
        abort("Aborting at user request.")

    with cd("/Users/lijian/Workspace/smart-buyer/spider"):
        run("git pull")
'''
