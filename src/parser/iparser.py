'''
Interface classes for parsing
'''


class IFileParser(object):

    def __init__(self, fileinfo):
        self._fileinfo = fileinfo
        self.m_strFile = ""
        self.m_bFileModified = False

    def isFileModified(self):
        return self.m_bFileModified

    def GetNumLineToIndex(self, iIndex=None):
        length = len(self.m_strFile)
        if iIndex is None:
            iIndex = length
        if length == 0 or iIndex > length:
            return 0
        iNumLine = 1
        iStart = 0
        while True:
            iStart = self.m_strFile.find('\n', iStart)
            if iStart == -1 or iIndex <= iStart or iStart + 1 == length:
                break
            iStart += 1
            iNumLine += 1
        return iNumLine

    def LoadFile(self):
        raise NotImplementedError()

    def SaveFile(self):
        raise NotImplementedError()

    def ClearMacro(self, FromId, ToId):
        raise NotImplementedError()

    def InsertMacro(self, index, Id):
        raise NotImplementedError()

    def Parse(self, mapfile):
        raise NotImplementedError()
