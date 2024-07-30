from unittest import TestCase
from parser.iparser import IFileParser
from mapfile.fileinfo import FileInfo


class TestIFileParser(TestCase):
    def test_Parse(self):
        f = FileInfo('test/tmp/file1')
        p = IFileParser(f)
        self.assertEqual("", p.m_strFile)
        self.assertFalse(p.m_bFileModified)

    def test_isFileModified(self):
        f = FileInfo('test/tmp/file1')
        p = IFileParser(f)
        self.assertFalse(p.isFileModified())
        p.m_bFileModified = True
        self.assertTrue(p.isFileModified())

    def test_GetNumLineToIndex_empty(self):
        strText = ""
        f = FileInfo('test/tmp/file1')
        p = IFileParser(f)
        p.m_strFile = strText
        self.assertEqual(0, p.GetNumLineToIndex())

    def test_GetNumLineToIndex_invalid(self):
        strText = ""
        f = FileInfo('test/tmp/file1')
        p = IFileParser(f)
        p.m_strFile = strText
        self.assertEqual(0, p.GetNumLineToIndex(10000))

    def test_GetNumLineToIndex_oneline(self):
        strText = "asd ddf e e4 44"
        f = FileInfo('test/tmp/file1')
        p = IFileParser(f)
        p.m_strFile = strText
        self.assertEqual(1, p.GetNumLineToIndex())

    def test_GetNumLineToIndex_treeline(self):
        strText = "asd \nddf e \nm4 44\n"
        f = FileInfo('test/tmp/file1')
        p = IFileParser(f)
        p.m_strFile = strText
        self.assertEqual(3, p.GetNumLineToIndex())

    def test_GetNumLineToIndex_fourline(self):
        strText = "asd \nddf e \nm4 44\nxxxx"
        f = FileInfo('test/tmp/file1')
        p = IFileParser(f)
        p.m_strFile = strText
        self.assertEqual(4, p.GetNumLineToIndex())

    def test_GetNumLineToIndex_treeline_index(self):
        strText = "asd \nddf e \nm4 44\n"
        index = strText.find('e')
        f = FileInfo('test/tmp/file1')
        p = IFileParser(f)
        p.m_strFile = strText
        self.assertEqual(2, p.GetNumLineToIndex(index))
