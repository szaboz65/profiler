'''
Interface classes for mapfile
'''

import os
import config

class IMapFileItem(object):
    USERDEF_MACRO_ID = 100
    USERDEF_MACRO_STR = "_user_defined_macro"

    # static variable
    __stId = USERDEF_MACRO_ID

    @staticmethod
    def getStartId():
        return IMapFileItem.__stId

    @staticmethod
    def setStartId(_id):
        IMapFileItem.__stId = _id

    @staticmethod
    def getNextId():
        IMapFileItem.__stId += 1
        return IMapFileItem.__stId

    def __init__(self):
        self.__Id = 0
        self.__NameSpace = ""
        self.__FileName = ""
        self.__FunctionName = ""
        self.__Line = 0

    def getId(self):
        return self.__Id

    def setId(self, _id):
        self.__Id = _id
    Id = property(getId, setId)

    def getNameSpace(self):
        return self.__NameSpace

    def setNameSpace(self, namespace):
        self.__NameSpace = namespace
    NameSpace = property(getNameSpace, setNameSpace)

    def getFileName(self):
        return self.__FileName

    def setFileName(self, filename):
        self.__FileName = filename
    FileName = property(getFileName, setFileName)

    def getFunctionName(self):
        return self.__FunctionName

    def setFunctionName(self, functionname):
        self.__FunctionName = functionname
    FunctionName = property(getFunctionName, setFunctionName)

    def getLine(self):
        return self.__Line

    def setLine(self, line):
        self.__Line = line
    Line = property(getLine, setLine)

    def GetFileNameWithLine(self):
        if len(self.FileName) == 0:
            return ""
        return self.FileName + " ln " + str(self.Line)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        string = ""
        if len(self.NameSpace) == 0 and len(self.FunctionName) == 0:
            string = str(self.Id)
            if self.Id < self.USERDEF_MACRO_ID:
                string += self.USERDEF_MACRO_STR
        else:
            if len(self.NameSpace) > 0:
                string += self.NameSpace + "::"
            string += self.FunctionName
        return string


class IMapFile(object):
    GROUP_LEVEL_CLASS = 1  # class
    GROUP_LEVEL_FILE = 2  # file
    GROUP_LEVEL_MODULE = 3  # extra before modules

    def __init__(self):
        self.__ProjectRootDir = ""
        self.__Items = []

    def get_ProjectRootDir(self):
        return self.__ProjectRootDir

    def set_ProjectRootDir(self, _dir):
        self.__ProjectRootDir = _dir
    ProjectRootDir = property(get_ProjectRootDir, set_ProjectRootDir)

    def getItemsCount(self):
        return len(self.__Items)

    def AddItems(self, item):
        if type(item) is list:
            self.__Items.extend(item)
        else:
            self.__Items.append(item)

    def ClearItems(self):
        self.__Items = []

    def getItem(self, idx):
        if idx >= len(self.__Items):
            raise Exception("Invalid itemindex")
        return self.__Items[idx]

    def GetLastId(self):
        n = self.getItemsCount()
        if n > 0:
            n = self.getItem(n-1).Id
        return n

    def GetGroupName(self, mapfileitem, groupLevel):
        if not (groupLevel > 0):
            raise Exception("Invalid Grouplevel")

        if groupLevel == self.GROUP_LEVEL_CLASS:
            return mapfileitem.NameSpace

        if groupLevel == self.GROUP_LEVEL_FILE:
            return mapfileitem.FileName

        groupName = ""
        path = mapfileitem.FileName
        if len(path) > len(self.__ProjectRootDir):
            relativPath = path[len(self.__ProjectRootDir):]
            dirs = relativPath.split(os.sep)
            groupLevel -= self.GROUP_LEVEL_MODULE - 1  # extra before modules
            i = 0
            if len(dirs[0]) == 0:
                groupLevel += 1
                i += 1
            if groupLevel <= len(dirs):
                while i < groupLevel:
                    if len(groupName):
                        groupName += os.sep
                    groupName += dirs[i]
                    i += 1
        return groupName

    def GetMapFileItem(self, _id):
        if len(self.__Items) == 0:
            raise Exception("Empty items")
        if not (_id < self.__Items[0].Id or self.__Items[-1].Id < _id):
            for item in self.__Items:
                if item.Id == _id:
                    return item
        raise Exception("Invalid item id")

    def AddNewMapFileItem(self, filename, line, namespace, functionname):
        raise NotImplementedError()
        # return id of the created mapfileitem
