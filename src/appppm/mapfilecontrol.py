'''
MapFileControl class
'''

import logging
import config
from mapfile.mapfile import MapFile
from mapfile.filecollector import FileCollector
from parser.fileparser import FileParser
from appppm.icontrol import IControl


class MapFileControl(IControl):

    def __init__(self, mapfiledir, detect_encoding=False):
        IControl.__init__(self)
        self.__detect_encoding = detect_encoding
        self._MapFile = MapFile(mapfiledir)

    def SetDefines(self, projectRoot, parseDirs, excludeDirs, excludeFiles, parseFiles):
        self._MapFile.ProjectRootDir = projectRoot

        self.parseFiles(parseDirs, excludeDirs, excludeFiles, parseFiles)

        self._MapFile.SaveMapFile()

        return True

    def ClearDefines(self, projectRoot, parseDirs, excludeDirs, excludeFiles, parseFiles):
        self.parseFiles(parseDirs, excludeDirs, excludeFiles, parseFiles, True)
        return True

    def parseFiles(self, parseDirs, excludeDirs, excludeFiles, parseFiles, bOnlyClear=False):
        fpc = FileCollector(excludeDirs, excludeFiles)
        fpc.CollectDirs(parseDirs)
        fpc.CollectFiles(parseFiles)
        for finfo in fpc.Files:
            if finfo.Extension != config.FILE_EXTENSION or finfo.Length < config.FILE_MIN_SIZE:
                continue

            strInfo = ("Clearing " if bOnlyClear else "Setting ") + finfo.FullName
            self.LastParsedFile = strInfo
            logging.info(strInfo)

            parser = FileParser(finfo, self.__detect_encoding)
            parser.LoadFile()
            parser.ClearMacro()

            if not bOnlyClear:
                parser.Parse(self._MapFile)

            if parser.isFileModified():
                parser.SaveFile()
