'''
Module to handle coverity files
'''

from statfile.istatfile import iCovFile
from statfile.csvfile import NumCsvFile


class CovFile(iCovFile):
    def LoadFile(self, fileinfo):
        if fileinfo.Exists:
            csv = NumCsvFile()
            csv.LoadFile(fileinfo.FullName)
            for data in csv.data:
                self.AddCovItem(data[0], data[1])
