'''
String utility routines for handle simplify generic extended string methods
'''


class StringUtils:

    @staticmethod
    def FindPrev(_str, index, c):
        index -= 1
        while index >= 0:
            if _str[index] == c:
                break
            index -= 1
        return index

    @staticmethod
    def FindPrevX(_str, index, c, cbad):
        iNum = 1
        index -= 1
        while index >= 0:
            if _str[index] == c:
                iNum -= 1
                if iNum == 0:
                    break
            if _str[index] == cbad:
                iNum += 1  # )) utan plusz egy nyitonak kell megallni
            index -= 1
        return index

    @staticmethod
    def GetCount(_str, c):
        count = 0
        for cstr in _str:
            if cstr == c:
                count += 1
        return count

    @staticmethod
    def RemoveComment(strLine):
        iComment1 = strLine.find("//")
        if iComment1 != -1:
            strLine = strLine[0: iComment1]
        iComment2 = strLine.find("/*")
        if iComment2 != -1:
            iComment2End = strLine.find("*/", iComment2)
            if iComment2End != -1:
                strPart1 = strLine[0: iComment2]
                strPart2 = strLine[iComment2End + 2:]
                return StringUtils.RemoveComment(strPart1 + strPart2)
            strLine = strLine[0: iComment2]
        return strLine

    @staticmethod
    def GetPrevLine(_str, iStart):
        if iStart < 0:
            return ""
        iHeaderPrevLine = StringUtils.FindPrev(_str, iStart, '\n')
        if iHeaderPrevLine == -1:
            return ""
        strPrevLine = _str[iHeaderPrevLine: iStart].strip()
        if strPrevLine.startswith("#") or strPrevLine == "" or strPrevLine.startswith("//"):
            return StringUtils.GetPrevLine(_str, iHeaderPrevLine - 1)
        strPrevLine = StringUtils.RemoveComment(strPrevLine)
        return strPrevLine
