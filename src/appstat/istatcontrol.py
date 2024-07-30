'''
Interface for coverity statistic control
'''


class iStatControl(object):
    def __init__(self):
        pass

    def parseCov(self, parseDir):
        raise NotImplementedError()

    def parseMap(self, mapfilename):
        raise NotImplementedError()

    def Save_AllFunc(self, filename):
        raise NotImplementedError()

    def Save_UnusedFunc(self, filename):
        raise NotImplementedError()

    def Save_UsedFunc(self, filename):
        raise NotImplementedError()

    def Save_AllStat(self, filename):
        raise NotImplementedError()
