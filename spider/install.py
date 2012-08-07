#!/bin/python
from fabric.api import local, settings, abort, run, cd
from fabric.api import task
from fabric.api import env
from fabric.operations import sudo
from fabric.contrib.console import confirm
from fabric.colors import green

def easyinstall(libname):
    with settings(warn_only=True):
        sudo("easy_install %s" % libname)
        print(green("success install %s" % libname))

@task
def redis():
    easyinstall('redis')

@task(default=True)
def all():
    redis()
