from unittest import TestCase
from mapfile.fileinfo import FileInfo
from parser.fileparser import FileParser


class TestFileParser(TestCase):
    def test_constr(self):
        f = FileInfo("test/file2.cpp")
        p = FileParser(f)
        self.assertEqual("", p.m_strFile)
        self.assertFalse(p.m_bFileModified)

    def test_ClearMacro_none(self):
        f = FileInfo("test/file2.cpp")
        p = FileParser(f)
        p.m_strFile = "int func(int param)\n{\n    return 0;\n}\n"
        p.ClearMacro()
        self.assertEqual("int func(int param)\n{\n    return 0;\n}\n", p.m_strFile)
        self.assertFalse(p.isFileModified())

    def test_ClearMacro_all(self):
        f = FileInfo("test/file2.cpp")
        p = FileParser(f)
        p.m_strFile = "int func(int param)\n{ SET_PPM(101)\n    return 0; SET_PPM(102)\n}\n"
        p.ClearMacro()
        self.assertEqual("int func(int param)\n{\n    return 0;\n}\n", p.m_strFile)
        self.assertTrue(p.isFileModified())

    def test_ClearMacro_first(self):
        f = FileInfo("test/file2.cpp")
        p = FileParser(f)
        p.m_strFile = "int func(int param)\n{ SET_PPM(101)\n    return 0; SET_PPM(102)\n}\n"
        p.ClearMacro(100, 101)
        self.assertEqual("int func(int param)\n{\n    return 0; SET_PPM(102)\n}\n", p.m_strFile)
        self.assertTrue(p.isFileModified())

    def test_ClearMacro_other(self):
        f = FileInfo("test/file2.cpp")
        p = FileParser(f)
        p.m_strFile = "int func(int param)\n{ SET_PPM(101)\n    return 0; SET_PPM(102)\n}\n"
        p.ClearMacro(102, 120)
        self.assertEqual("int func(int param)\n{ SET_PPM(101)\n    return 0;\n}\n", p.m_strFile)
        self.assertTrue(p.isFileModified())

    def test_ClearMacro_invalid(self):
        f = FileInfo("test/file2.cpp")
        p = FileParser(f)
        p.m_strFile = "int func(int param)\n{ SET_PPM(101)\n    return 0; SET_PPM(102)\n}\n"
        p.ClearMacro(1000, 2000)
        self.assertEqual("int func(int param)\n{ SET_PPM(101)\n    return 0; SET_PPM(102)\n}\n", p.m_strFile)
        self.assertFalse(p.isFileModified())

    def test_InsertMacro(self):
        f = FileInfo("test/file2.cpp")
        p = FileParser(f)
        p.m_strFile = "int func(int param)\n{\n    return 0;\n}\n"
        p.InsertMacro(p.m_strFile.find('{')+1, 101)
        self.assertEqual("int func(int param)\n{ SET_PPM(101)\n    return 0;\n}\n", p.m_strFile)
        self.assertTrue(p.isFileModified())

    def test_Save_LoadFile_uncoded(self):
        f = FileInfo("test/file2.cpp")
        p = FileParser(f)
        p.m_strFile = "int func(int param)\n{\n    return 0;\n}\n"
        p.InsertMacro(p.m_strFile.find('{')+1, 101)  # only set filemodified flag
        p.SaveFile()
        self.assertFalse(p.isFileModified())
        p.InsertMacro(p.m_strFile.find('{')+1, 102)  # only set filemodified flag
        p.LoadFile()
        self.assertEqual("int func(int param)\n{ SET_PPM(101)\n    return 0;\n}\n", p.m_strFile)
        self.assertFalse(p.isFileModified())

    def test_Parse(self):
        class MockMapFile(object):
            def AddNewMapFileItem(self, filename, line, namespace, functionname):
                self.FileName = filename
                self.Line = line
                self.NameSpace = namespace
                self.FunctionName = functionname
                return 111

        mockmapfile = MockMapFile()
        f = FileInfo("test/file2.cpp")
        p = FileParser(f)
        p.m_strFile = "int class::func(int param)\n{\n    return 0;\n}\n"
        p.Parse(mockmapfile)
        self.assertEqual("int class::func(int param)\n{ SET_PPM(111)\n    return 0;\n}\n", p.m_strFile)
        self.assertTrue(p.isFileModified())
        self.assertEqual("test/file2.cpp", mockmapfile.FileName)
        self.assertEqual(2, mockmapfile.Line)
        self.assertEqual("class", mockmapfile.NameSpace)
        self.assertEqual("func", mockmapfile.FunctionName)
