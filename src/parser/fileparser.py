'''
Module to handle block in file
'''

import logging
import config
from parser.iparser import IFileParser
from parser.iblock import BlockType
from parser.blockparserbase import BlockParserBase
from parser.block import Block
from parser.coding import Coding
from mapfile.fileinfo import File


class BlockParser(BlockParserBase):
    def CreateBlock(self, parent, iStart, iEnd):
        return Block(parent, self.strText, iStart, iEnd)


class FileParser(IFileParser):

    def __init__(self, fileinfo, detect_encoding=False):
        IFileParser.__init__(self, fileinfo)
        self.__DetectEncoding = detect_encoding
        self.__Encoder = None

    def Parse(self, mapfile):
        blockparser = BlockParser(self.m_strFile)
        blocks = blockparser.GetBlocks()

        for block in reversed(blocks):
            if block.m_Type == BlockType.FUNCTION:
                line = self.GetNumLineToIndex(block.m_iStart)
                Id = mapfile.AddNewMapFileItem(self._fileinfo.FullName, line, block.GetNamespace(),
                                               block.GetFunctionName())
                self.InsertMacro(block.m_iStart + 1, Id)
                logging.debug("Insert macro into %s line %s, %s::%s, %s", self._fileinfo.FullName, str(line),
                              block.GetNamespace(), block.GetFunctionName(), Id)

    def LoadFile(self):
        self.m_strFile = ""
        if not self._fileinfo.Exists:
            return
        if self.__DetectEncoding:
            coding = Coding(self._fileinfo.FullName)
            if coding is not None:
                self.__Encoder = coding
        if self.__Encoder is not None:
            self.m_strFile = self.__Encoder.readFile()
        else:
            self.m_strFile = File.ReadAllText(self._fileinfo.FullName)
        self.m_bFileModified = False

    def SaveFile(self):
        if self.__Encoder is not None:
            if self.__Encoder.writeFile(self.m_strFile):
                self.m_bFileModified = False
        else:
            if File.WriteAllText(self._fileinfo.FullName, self.m_strFile):
                self.m_bFileModified = False

    def InsertMacro(self, index, Id):
        strMacro = config.MACRO_BEGIN + str(Id) + config.MACRO_END
        self.m_strFile = self.m_strFile[:index] + strMacro + self.m_strFile[index:]
        self.m_bFileModified = True

    def ClearMacro(self, FromId=0, ToId=0):
        iStart = 0
        while True:
            iStart = self.m_strFile.find(config.MACRO_BEGIN, iStart)
            if iStart == -1:
                break

            iEnd = self.m_strFile.find(config.MACRO_END, iStart)
            if ToId != 0:
                strId = self.m_strFile[iStart + len(config.MACRO_BEGIN): iEnd]
                _id = int(strId)
                if _id < FromId or ToId < _id:
                    iStart = iEnd
                    continue

            self.m_strFile = self.m_strFile[:iStart] + self.m_strFile[iEnd + len(config.MACRO_END):]
            self.m_bFileModified = True
