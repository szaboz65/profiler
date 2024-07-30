'''
MapFile model
'''

import os
import logging
import config
from mapfile.imapfile import IMapFileItem, IMapFile


class MapFileItem(IMapFileItem):

    def __init__(self, line=None, _id=None):
        IMapFileItem.__init__(self)

        if _id is not None:
            self.Id = _id

        elif line is not None:
            tokens = line.split(config.SEPARATOR)
            if not (len(tokens) == 5):
                raise Exception("Missing token")
            self.Id = int(tokens[0])
            self.NameSpace = tokens[1]
            self.FunctionName = tokens[2]
            self.FileName = tokens[3]
            self.Line = int(tokens[4])

        else:
            raise Exception("Missing parameter")

    def GetMapFileLine(self):
        self.NameSpace = self.NameSpace.replace(config.SEPARATOR, ',')
        self.FunctionName = self.FunctionName.replace(config.SEPARATOR, ',')
        self.FileName = self.FileName.replace(config.SEPARATOR, ',')
        line = str(self.Id)
        line += config.SEPARATOR + self.NameSpace
        line += config.SEPARATOR + self.FunctionName
        line += config.SEPARATOR + self.FileName
        line += config.SEPARATOR + str(self.Line)
        return line


class MapFile(IMapFile):

    def __init__(self, mapfiledir='.'):
        IMapFile.__init__(self)
        self.mapfiledir = mapfiledir

    def GetFilename(self):
        return os.path.normpath(os.path.join(self.mapfiledir, config.MAPFILE_NAME))

    def AddNewMapFileItem(self, filename, line, namespace, functionname):
        Id = MapFileItem.getNextId()
        mapFileItem = MapFileItem(_id=Id)
        mapFileItem.FileName = filename
        mapFileItem.Line = line
        mapFileItem.NameSpace = namespace
        mapFileItem.FunctionName = functionname
        self.AddItems(mapFileItem)
        return Id

    def GetMapFileItem(self, _id):
        if self.getItemsCount() == 0 or _id < self.getItem(0).Id or self.getItem(-1).Id < _id:
            return MapFileItem(_id=_id)

        n = self.getItemsCount()
        i = 0
        while i < n:
            if self.getItem(i).Id == _id:
                return self.getItem(i)
            i += 1
        raise Exception("Invalid itemid")

    def LoadMapFile(self, filename=None):
        if filename is None:
            filename = self.GetFilename()

        if not os.path.isfile(filename):
            logging.error("Mapfile cannot found: %s", filename)
            return False

        self.ClearItems()
        with open(filename) as f:
            lines = f.read().splitlines()
            if len(lines) == 0:
                return True

            self.ProjectRootDir = lines[0]
            i = 1
            while i < len(lines):
                self.AddItems(MapFileItem(line=lines[i]))
                i += 1
            logging.info("Mapfile loadded successfully: %s", filename)
            return True
        return False

    def SaveMapFile(self, filename=None):
        if filename is None:
            filename = self.GetFilename()
        with open(filename, 'w') as f:
            f.write(self.ProjectRootDir if self.ProjectRootDir is not None else '')
            f.write("\n")
            for i in range(self.getItemsCount()):
                f.write(self.getItem(i).GetMapFileLine())
                f.write("\n")
            logging.info("Mapfile saved successfully: %s", filename)
