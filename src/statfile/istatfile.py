'''
Interface for coverity statistic files
'''


class iCovFile(object):

    def __init__(self, size):
        self.cov = [0] * size

    def GetCovCount(self):
        return len(self.cov)

    def AddCovItem(self, _id, count):
        if _id < self.GetCovCount():
            self.cov[_id] += count

    def getCovItems(self):
        return self.cov

    def LoadFile(self, fileinfo):
        pass


class iStatFile(object):
    def CreateCSV(self, mapfile, covs):
        pass
