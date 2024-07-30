'''
Module to parse blocks
'''

from parser.iblock import BlockType, iBlock
from parser.stringutils import StringUtils


class Block(iBlock):

    def __init__(self, parent, _str, iStart, iEnd):
        iBlock.__init__(self, parent)
        if parent is not None and parent.m_iEnd > iStart:
            self.m_Parent = parent  # parent block: (ex namespace)
        else:
            self.m_Parent = None
        self.m_str = _str  # full file
        self.m_iStart = iStart  # the starting point in m_strBody
        self.m_iEnd = iEnd  # the ending point in m_strBody
        self.m_strHeader = ""  # usually the previous line, it contains: class,namespace,function
        self.Init()

    def Init(self):
        if self.IsMacroBlock():
            self.m_Type = BlockType.MACRO
            return

        self.m_strHeader = self.InitHeader(self.m_iStart)
        self.m_strHeader = self.m_strHeader.replace('\t', ' ')
        if self.m_strHeader == "":
            self.m_Type = BlockType.UNKNOWN
            return
        if self.m_strHeader.endswith("="):
            self.m_Type = BlockType.ARRAY
            return

        if self.InitNamespace(self.m_strHeader):
            self.m_Type = BlockType.NAMESPACE
            return

        if self.m_strHeader.find("class ") != -1 or self.m_strHeader.find("struct ") != -1 \
                or self.m_strHeader.endswith("class") or self.m_strHeader.endswith("struct"):
            self.m_Type = BlockType.CLASSSTRUCT
            return
        if self.m_strHeader.find("enum ") != -1:
            self.m_Type = BlockType.ENUM
            return
        if self.m_strHeader.find("typedef ") != -1:
            self.m_Type = BlockType.TYPEDEF
            return
        if self.m_strHeader.find("extern ") != -1:
            self.m_Type = BlockType.EXTERN
            return
        if self.m_strHeader.find("union ") != -1:
            self.m_Type = BlockType.UNION
            return
        if self.InitFunction(self.m_strHeader):
            self.m_Type = BlockType.FUNCTION
            return

        strBody = self.GetText()
        if strBody.find("__try") != -1:
            self.m_Type = BlockType.TRYCATCH

    def InitHeader(self, iStart):
        iPrevLine = StringUtils.FindPrev(self.m_str, max([iStart-1, 0]), '\n')
        if iPrevLine == -1:
            iPrevLine = 0

        strHeader = self.m_str[iPrevLine: iStart]
        iHeaderLength = len(strHeader)
        iHeaderStart = iPrevLine

        if iHeaderLength == 0:
            return ""

        # ures sor, konstruktor member inicializalas skip
        strHeaderTrimmed = strHeader.strip()
        if strHeaderTrimmed == "" \
                or strHeaderTrimmed.startswith(",") \
                or strHeaderTrimmed.startswith(":") \
                or strHeaderTrimmed.startswith("//") \
                or strHeaderTrimmed.startswith("#"):
            return self.InitHeader(iHeaderStart)

        strHeader = StringUtils.RemoveComment(strHeader)
        if strHeader.find(')') > -1:
            if StringUtils.GetCount(strHeader, '(') == StringUtils.GetCount(strHeader, ')'):
                iBracketStart = strHeader.find("(")
                iBracketEnd = len(strHeader)  # StringUtils.FindPrev(strHeader, len(strHeader), ')')
                strPart1 = strHeader[0: iBracketStart]
                strPart2 = strHeader[iBracketEnd + 1:]
                strHeader = strPart1 + strPart2
            else:
                iBracketEnd = StringUtils.FindPrev(self.m_str, iHeaderStart + iHeaderLength + 1, ')')
                if not (iBracketEnd >= iHeaderStart):
                    raise Exception("Missing Bracket")
                iBracketStart = StringUtils.FindPrevX(self.m_str, iBracketEnd, '(', ')')
                if iBracketStart == -1:
                    raise Exception("Unbalanced Brackets")
                return self.InitHeader(iBracketStart)

        # prev line
        strPrevLine = StringUtils.GetPrevLine(self.m_str, iHeaderStart)
        strPrevLine = strPrevLine.strip()
        if strPrevLine.endswith(",") or (strPrevLine.endswith(":") and not strPrevLine.endswith("::")):
            return self.InitHeader(iHeaderStart - 1)

        strHeader = strHeader.strip()
        iPrevHeader = StringUtils.FindPrev(self.m_str, max([iHeaderStart-1, 0]), '\n')
        if iPrevHeader != -1:
            strPrevHeader = self.m_str[iPrevHeader: iHeaderStart]
            strPrevHeader = strPrevHeader.strip()
            if strPrevHeader.endswith("::"):
                strHeader = strPrevHeader + strHeader

        return strHeader

    def InitNamespace(self, strHeader):
        strNamespace = "namespace"
        iNameSpace = strHeader.find(strNamespace)
        if iNameSpace == -1:
            return False
        iStart = iNameSpace + len(strNamespace) + 1
        if iStart < len(strHeader):
            self.m_strNamespace = strHeader[iStart:].strip()
        return True

    def InitFunction(self, strHeader):
        iFunctionEnd = strHeader.find('(')
        if iFunctionEnd == -1:
            iFunctionEnd = len(strHeader)
        if iFunctionEnd == 0:
            return False

        tokens = strHeader[:iFunctionEnd].split(' ')
        strHeader = tokens[-1]
        while strHeader[0] == '*' or strHeader[0] == '&':
            strHeader = strHeader[1:]

        iFunctionStart = 0
        iFunctionEnd = len(strHeader)
        iNameSpaceEnd = strHeader.rfind("::")
        if iNameSpaceEnd != -1 and iNameSpaceEnd < iFunctionEnd:
            iFunctionStart = iNameSpaceEnd + 2
            iNameSpaceStart = 0
            self.m_strNamespace = strHeader[iNameSpaceStart: iNameSpaceEnd].strip()

        if iFunctionEnd <= iFunctionStart:
            return False

        self.m_strFunctionName = strHeader[iFunctionStart: iFunctionEnd].strip()
        return True

    def IsMacroBlock(self):
        for i in range(self.m_iStart, min([self.m_iEnd+1, len(self.m_str)])):
            if self.m_str[i] != '\n':
                continue
            return self.m_str[i - 1] == '\\' or self.m_str[i - 2] == '\\'
        return False

    def GetText(self):
        return self.m_str[self.m_iStart: self.m_iEnd]
