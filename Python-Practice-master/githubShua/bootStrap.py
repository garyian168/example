#!/usr/bin/env python
# coding: utf-8

import subprocess
import os
from config import config


def editDate():
    subprocess.call('date -s "%s"' % config["dest_date"], shell=True)


def showDate():
    subprocess.call("date", shell=True)


def enterDir():
    os.chdir(config["path_to_dir"])

    if not os.path.exists("test"):
        subprocess.call("mkdir test", shell=True)

    os.chdir("test")


def editFile():
    with open(config["file_name"], "w") as f:
        f.write(config["dest_date"])


def gitConfig():
    subprocess.call("git init", shell=True)
    subprocess.call("git remote add origin git@github.com:%s/Test.git" % config["github_name"], shell=True)
    subprocess.call('git config --local user.email "%s"' % config["github_email"], shell=True)
    subprocess.call('git config --local user.name "%s"' % config["github_name"], shell=True)
    subprocess.call("git pull origin master", shell=True)


def gitCommit():
    subprocess.call("git add .", shell=True)
    subprocess.call('git commit -m "%s"' % config["dest_date"], shell=True)
    subprocess.call("git push origin master", shell=True)


if __name__ == "__main__":
    enterDir()
    gitConfig()

    editDate()
    editFile()

    gitCommit()
