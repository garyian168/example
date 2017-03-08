#!/usr/bin/env python

import subprocess
import time
import sys

"""Subtube is module that simplifies and automates some aspects of subprocess"""

class BaseArgs(object):
    """Base Argument Class that handles keyword argument parsing"""

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

        if self.kwargs.has_key("delay"):
            self.delay = self.kwargs["delay"]
        else:
            self.delay = 0

        if self.kwargs.has_key("verbose"):
            self.verbose = self.kwargs["verbose"]
        else:
            self.verbose = False

    def run(self):
        """You must implement a run method"""
        raise NotImplementedError


class Runner(BaseArgs):

    def run(self):
        for cmd in self.args:
            if self.verbose:
                print "Running %s with delay=%s" % (cmd, self.delay)
            time.sleep(self.delay)
            subprocess.call(cmd, shell=True)

if __name__ == "__main__":
    r = Runner("ls", "pwd", verbose=True)
    r.run()
