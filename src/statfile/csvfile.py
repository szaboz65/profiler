'''
Module to handle csv files
'''

from mapfile.fileinfo import File


class CsvFile(object):
    SEPARATOR = ';'
    NEWLINE = '\n'

    def __init__(self):
        self.header = []
        self.data = []

    def Clear(self):
        self.header = []
        self.data = []

    def SetHeader(self, *arg):
        self.header = []
        for a in arg:
            self.header.append(a)

    def AddData(self, *arg):
        if len(arg) != len(self.header):
            return
        data = []
        for a in arg:
            data.append(a)
        self.data.append(data)

    def ToString(self):
        strText = self.SEPARATOR.join(self.header)
        for data in self.data:
            strData = self.SEPARATOR.join(self.formatData(data))
            strText = self.NEWLINE.join([strText, strData])
        return strText + self.NEWLINE

    def formatData(self, data):
        return data

    def parseString(self, strText):
        self.Clear()
        lines = strText.split(self.NEWLINE)
        first_line = True
        for line in lines:
            if len(line) == 0:
                continue
            parts = line.split(self.SEPARATOR)
            if first_line:
                first_line = False
                self.header.extend(parts)
            else:
                self.data.append(self.parseData(parts))

    def parseData(self, parts):
        return parts

    def SaveFile(self, filename):
        return File.WriteAllText(filename, self.ToString())

    def LoadFile(self, filename):
        strText = File.ReadAllText(filename)
        self.parseString(strText)


class NumCsvFile(CsvFile):
    def formatData(self, data):
        return [str(x) for x in data]

    def parseData(self, data):
        return [int(x) for x in data]
