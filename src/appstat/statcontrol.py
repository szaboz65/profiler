'''
Statistic control module
'''

import logging
import config
from mapfile.mapfile import MapFile
from mapfile.filecollector import FileCollector
from statfile.covfile import CovFile
from statfile.statfile import StatData, StatFunc
from appstat.istatcontrol import iStatControl


class StatControl(iStatControl):

    def __init__(self):
        iStatControl.__init__(self)
        self.MapFile = None
        self.CovFile = None

    def parseMap(self, mapfilename):
        self.MapFile = MapFile("")
        return self.MapFile.LoadMapFile(filename=mapfilename)

    def parseCov(self, parseDir):
        self.CovFile = CovFile(self.MapFile.GetLastId()+1)
        fpc = FileCollector()
        fpc.CollectDirs(parseDir)
        for finfo in fpc.Files:
            if finfo.Extension == config.COVFILE_EXTENSION:
                logging.debug("Parse: " + finfo.FullName)
                self.CovFile.LoadFile(finfo)

    def Save_AllFunc(self, filename):
        s = StatFunc()
        return s.CreateCSV(self.MapFile, self.CovFile.getCovItems()).SaveFile(filename)

    def Save_UnusedFunc(self, filename):
        s = StatFunc()
        return s.CreateCSV(self.MapFile, filter(lambda data: data == 0, self.CovFile.getCovItems())).SaveFile(filename)

    def Save_UsedFunc(self, filename):
        s = StatFunc()
        return s.CreateCSV(self.MapFile, filter(lambda data: data != 0, self.CovFile.getCovItems())).SaveFile(filename)

    def Save_AllStat(self, filename):
        s = StatData()
        return s.CreateCSV(self.MapFile, self.CovFile.getCovItems()).SaveFile(filename)
