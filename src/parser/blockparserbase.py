'''
Module to parse block base
'''

from parser.iblock import BlockType, iBlockParser


class BlockParserBase(iBlockParser):

    def GetBlocks(self):
        self.index = 0
        blocks = []
        parent = None
        while True:
            block = self.GetNextBlock(parent)
            if block is None:
                return blocks

            if block.m_Type == BlockType.UNKNOWN:
                continue

            if block.m_Type != BlockType.NAMESPACE and block.m_Type != BlockType.FUNCTION:
                continue

            blocks.append(block)
            if block.m_Type == BlockType.NAMESPACE:
                self.index = block.m_iStart + 1
                parent = block

            while parent is not None and block.m_iStart > parent.m_iEnd:
                parent = parent.m_Parent

    def GetNextBlock(self, parent):
        iBlockStart = self.index
        iDepth = 0
        while self.index < len(self.strText):
            if self.SkipIfNeed():
                continue
            if self.strText[self.index] == '{':
                if iDepth == 0:
                    iBlockStart = self.index
                iDepth += 1

            if self.strText[self.index] == '}':
                if iDepth > 0:
                    iDepth -= 1
                    if iDepth == 0:
                        self.index += 1
                        block = self.CreateBlock(parent, iBlockStart, self.index)
                        return block

            self.index += 1
        return None

    def SkipIfDef(self):
        iNextIf = self.strText.find("#if", self.index)
        if iNextIf == -1:
            return False
        iEndIf = self.strText.find("#endif", self.index)
        if iEndIf == -1:
            raise Exception("Missing #endif")
        if iNextIf > iEndIf:
            return  False

        self.index = iNextIf + 1
        if self.SkipIfDef():
            iEndIf = self.strText.find("#endif", self.index)
            if iEndIf == -1:
                raise Exception("Missing #endif")

        self.index = iEndIf
        self.FindNextLine()
        return True

    def SkipIfNeed(self):
        if self.index + 2 <= len(self.strText) and self.strText[self.index : self.index + 2] == '//':  # comment
            self.FindNextLine()
            return True

        if self.strText[self.index] == '"':
            self.SkipQuotation()
            return True

        if self.index + 4 <= len(self.strText) and self.strText[self.index : self.index + 2] == '/*':  # /* kezelese */
            self.index = self.strText.find("*/", self.index+2)
            if not (self.index != -1):
                raise Exception("Outstanding comment")
            self.index += 2
            return True

        if self.strText[self.index] == '#':  # skip define
            while True:
                iStart = self.index
                self.FindNextLine()
                if iStart < self.index - 3:
                    c = self.strText[self.index - 3]
                    if self.strText[self.index - 3 : self.index - 1] != '\\\\':
                        break
            return True

        return False

    def FindNextLine(self):
        while self.index < len(self.strText) - 1:
            self.index += 1
            if (self.strText[self.index-1] == '\n'):
                break

    def SkipQuotation(self):
        if self.IsFalseQuotation():
            self.index += 1
            return

        while True:
            if self.index + 1 >= len(self.strText):  # a kovetkezo karaktertol menne a kereses, az meg a stringbe esik-e?
                self.index += 1
                return

            self.index = self.strText.find('"', self.index + 1)
            if not (self.index != -1):
                raise Exception("")
            if self.index == -1:
                return
            if self.IsFalseQuotation():
                continue
            break
        self.index += 1

    def IsFalseQuotation(self):
        if self.index == 0:
            return False
        if self.strText[self.index - 1] == '\'' and self.strText[self.index + 1] == '\'':
            return True  # '"'
        iNumPer = 0
        index = self.index
        while index > 0:
            index -= 1
            if self.strText[index] != '\\':  # "" kozott van egy " agyazva pl:   print(" valami \"=idezojel");
                break
            iNumPer += 1

        if iNumPer % 2 == 1:
            return True
        return False

