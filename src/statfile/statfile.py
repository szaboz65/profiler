'''
Module to make statistic files
'''

from statfile.istatfile import iStatFile
from statfile.csvfile import CsvFile
from mapfile.mapfile import MapFile


class StatNode(object):
    def __init__(self, count=0):
        self.__count = count
        self.__used = 0

    def get_count(self):
        return self.__count

    def set_count(self, count):
        self.__count = count
    Count = property(get_count, set_count)

    def get_used(self):
        return self.__used

    def set_used(self, used):
        self.__used = used
    Used = property(get_used, set_used)

    def get_unused(self):
        return self.Count - self.Used
    Unused = property(get_unused)

    def AddCount(self, count):
        self.__count += count

    def AddUsed(self, used):
        self.__used += used


class StatData(iStatFile):

    def __init__(self):
        iStatFile.__init__(self)
        self.stat = {}

    def CollectMap(self, mapfile):
        self.stat = {}
        idx = 0
        while idx < mapfile.getItemsCount():
            item = mapfile.getItem(idx)
            idx += 1
            i = 0
            while True:
                key = mapfile.GetGroupName(item, MapFile.GROUP_LEVEL_MODULE + i)
                i += 1
                if len(key) == 0:
                    break
                if key not in self.stat:
                    self.stat[key] = StatNode(1)
                else:
                    self.stat[key].AddCount(1)

    def CollectUsed(self, mapfile, covs):
        idx = 0
        while idx < len(covs):
            if covs[idx] != 0:
                item = mapfile.GetMapFileItem(idx)
                i = 0
                while True:
                    key = mapfile.GetGroupName(item, MapFile.GROUP_LEVEL_MODULE + i)
                    i += 1
                    if len(key) == 0:
                        break
                    if key in self.stat:
                        self.stat[key].AddUsed(1)
            idx += 1

    def CreateCSV(self, mapfile, covs):
        self.CollectMap(mapfile)
        self.CollectUsed(mapfile, covs)
        csv = CsvFile()
        csv.SetHeader("method_count", "used_method_count", "unused_method_count",
                      "used_method_percent", "unused_method_percent", "path")
        for key, data in self.stat.items():
            csv.AddData(str(data.Count), str(data.Used), str(data.Unused),
                        '{0:.2f}%'.format(100.0*data.Used/data.Count),
                        '{0:.2f}%'.format(100.0*data.Unused/data.Count), key)
        return csv


class StatFunc(iStatFile):
    def CreateCSV(self, mapfile, covs):
        csv = CsvFile()
        csv.SetHeader("method_id", "class_name", "method_name", "source_file", "line_num", "count")
        _id = 0
        while _id < len(covs):
            m = mapfile.GetMapFileItem(_id)
            if m.Line:
                csv.AddData(str(m.Id), m.NameSpace, m.FunctionName, m.FileName, str(m.Line), str(covs[_id]))
            _id += 1
        return csv
