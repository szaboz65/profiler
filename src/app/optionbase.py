'''
Options for general usage
'''

import sys


class OptionBase(object):
    EXIT = 0
    OK = 1
    ERROR = 2

    def __init__(self):
        self._isDebug = False
        self._isVerbose = False
        self._isLog = False

    def get_isDebug(self):
        return self._isDebug
    isDebug = property(get_isDebug)

    def get_isVerbose(self):
        return self._isVerbose
    isVerbose = property(get_isVerbose)

    def get_isLog(self):
        return self._isLog
    isLog = property(get_isLog)

    def isWindows(self):
        """
        Check the system is Windows
        :rtype : bool
        """
        return sys.platform.startswith("win")

    # virtuals
    def loadOptions(self, appname, argv):
        pass
