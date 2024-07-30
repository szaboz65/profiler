'''
Module to collect files recursively
'''

from mapfile.fileinfo import FileInfo, DirectoryInfo
import os


class FileCollector(object):
    def __init__(self, excludeDirs=[], excludeFiles=[]):
        self.__excludeDirs = []
        self.__excludeFiles = []
        self.__files = []
        self.AddExcludeDir(excludeDirs)
        self.AddExcludeFile(excludeFiles)

    def GetFilesCount(self):
        return len(self.__files)

    def AddFiles(self, files):
        if type(files) is list:
            self.__files.extend(files)
        else:
            self.__files.append(files)

    def ClearFiles(self):
        self.__files = []

    def get_files(self):
        return self.__files
    Files = property(get_files)

    def AddExcludeDir(self, _dir):
        if type(_dir) == str:
            _dir = [_dir]
        for d in _dir:
            self.__excludeDirs.append(os.path.normpath(d))

    def IsExcludeDir(self, _dir):
        _dir = os.path.normpath(_dir)
        for excdir in self.__excludeDirs:
            if _dir.startswith(excdir):
                return True
        return False

    def AddExcludeFile(self, filename):
        if type(filename) == str:
            filename = [filename]
        for f in filename:
            self.__excludeFiles.append(os.path.normpath(f))

    def IsExcludeFile(self, filename):
        filename = os.path.normpath(filename)
        for excfile in self.__excludeFiles:
            if filename.startswith(excfile):
                return True
        return False

    def CollectDirs(self, parseDirs=None):
        if parseDirs is not None:
            if type(parseDirs) == str:
                parseDirs = [parseDirs]
            for _dir in parseDirs:
                self.AddDirectory(DirectoryInfo(_dir))

    def CollectFiles(self, parseFiles=None):
        if parseFiles is not None:
            if type(parseFiles) == str:
                parseFiles = [parseFiles]
            for file in parseFiles:
                self.AddFiles(FileInfo(file))

    def AddDirectory(self, dirinfo):
        if self.IsExcludeDir(dirinfo.Name):
            return
        for f in dirinfo.GetFiles():
            if not self.IsExcludeFile(f.FullName):
                self.AddFiles(f)
        for d in dirinfo.GetDirectories():
            self.AddDirectory(d)
