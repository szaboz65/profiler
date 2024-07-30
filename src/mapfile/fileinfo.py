'''
Module to handle C# like  File, FileInfo and DirectoryInfo Classes
'''

import os


class File(object):
    @staticmethod
    def ReadAllText(FileName):
        if File.Exists(FileName):
            with open(FileName, "rt") as f:
                return f.read()
        return ""

    @staticmethod
    def WriteAllText(FileName, _str):
        with open(FileName, "wt") as f:
            f.write(_str)
            return True
        return False

    @staticmethod
    def Exists(FileName):
        return os.path.isfile(FileName)

    @staticmethod
    def FileSize(FileName):
        return os.path.getsize(FileName)

    @staticmethod
    def FindFile(DirName, FileName):
        for root, dirs, files in os.walk(DirName):
            if FileName in files:
                return os.path.normpath(os.path.join(root, FileName))
        return None

    @staticmethod
    def Delete(Filename):
        os.remove(Filename)


class FileInfo(object):

    def __init__(self, filepath):
        self.__filepath = filepath

    def get_Extension(self):
        filename, file_extension = os.path.splitext(self.__filepath)
        return file_extension
    Extension = property(get_Extension)

    def get_Name(self):
        filename, file_extension = os.path.splitext(self.__filepath)
        return filename
    Name = property(get_Name)

    def get_FullName(self):
        return self.__filepath
    FullName = property(get_FullName)

    def get_Size(self):
        return File.FileSize(self.__filepath)
    Length = property(get_Size)

    def is_Exist(self):
        return File.Exists(self.__filepath)
    Exists = property(is_Exist)


class DirectoryInfo(object):
    def __init__(self, root):
        self.__root = os.path.normpath(root)
        self.__dirlist = []
        self.__filelist = []

        if not os.path.isdir(root):
            return

        for item in os.listdir(root):
            if item == '.' or item == '..':
                continue
            path = os.path.normpath(os.path.join(root, item))
            if os.path.isfile(path):
                self.__filelist.append(path)
            elif os.path.isdir(path):
                self.__dirlist.append(path)

    def get_Name(self):
        return self.__root
    Name = property(get_Name)

    def GetDirectories(self):
        return [DirectoryInfo(d) for d in self.__dirlist]

    def GetFiles(self):
        return [FileInfo(f) for f in self.__filelist]
