#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import with_statement

#设置shell
from fabric.api import env
env.shell = "/bin/sh -c"

from fabric.api import settings, run,execute
from fabric.api import *
from fabric.contrib.console import confirm
from fabric.colors import green

def hello_word():
	print(green("hello world"))