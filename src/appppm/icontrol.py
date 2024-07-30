'''
Interface classes for control
'''


class IControl(object):
    def __init__(self):
        self._LastParsedFile = ""

    def get_LastParsedFile(self):
        return self._LastParsedFile

    def set_LastParsedFile(self, f):
        self._LastParsedFile = f
    LastParsedFile = property(get_LastParsedFile, set_LastParsedFile)

    def SetDefines(self, projectRoot, parseDirs, excludeDirs, excludeFiles, parseFiles):
        raise NotImplementedError()

    def ClearDefines(self, projectRoot, parseDirs, excludeDirs, excludeFiles, parseFiles):
        raise NotImplementedError()
