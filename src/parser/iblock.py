'''
Interface for blocks
'''


class BlockType:
    FUNCTION = 0
    NAMESPACE = 1
    CLASSSTRUCT = 2
    ARRAY = 3
    MACRO = 4
    ENUM = 5
    TRYCATCH = 6
    TYPEDEF = 7
    EXTERN = 8
    UNION = 9
    UNKNOWN = 10


class iBlock(object):
    def __init__(self, parent=None):
        self.m_Parent = parent
        self.m_Type = BlockType.UNKNOWN
        self.m_strNamespace = ""
        self.m_strFunctionName = ""

    def GetParent(self):
        return self.m_Parent

    def GetFunctionName(self):
        return self.m_strFunctionName

    def GetNamespace(self):
        strNamespace = ""
        if self.m_Parent is not None:
            strNamespace = self.m_Parent.GetNamespace()
            if self.m_strNamespace is not None and len(self.m_strNamespace) > 0:
                strNamespace += "::"
        return strNamespace + self.m_strNamespace

    def __str__(self):
        _str = ""
        if self.m_strNamespace is not None and len(self.m_strNamespace) > 0:
            _str = self.m_strNamespace + "::"
        return _str + self.m_strFunctionName

    def __repr__(self):
        return self.__str__()


class iBlockParser(object):
    def __init__(self, strText):
        self.strText = strText
        self.index = 0

    def CreateBlock(self, parent, iStart, iEnd):
        raise NotImplementedError()
        # return None or iBlock

    def GetBlocks(self):
        raise NotImplementedError()
        # return [] list of iBlock
