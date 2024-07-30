from unittest import TestCase
from mapfile.mapfile import MapFileItem, MapFile
import config
import os


class TestMapFileItem(TestCase):
    def test_const(self):
        with self.assertRaises(Exception) as cm:
            m = MapFileItem()
            self.fail()

        self.assertTrue("Missing parameter" in str(cm.exception))

    def test_const_id(self):
        m = MapFileItem(_id=123)
        self.assertEqual(123, m.Id)

        self.assertEqual('123;;;;0', m.GetMapFileLine())

    def test_const_line_token0(self):
        with self.assertRaises(Exception) as cm:
            m = MapFileItem(line="asd")
            self.fail()

        self.assertTrue("Missing token" in str(cm.exception))

    def test_const_line_token4(self):
        with self.assertRaises(Exception) as cm:
            m = MapFileItem(line="1;2;3;4")
            self.fail()

        self.assertTrue("Missing token" in str(cm.exception))

    def test_const_line_token6(self):
        with self.assertRaises(Exception) as cm:
            m = MapFileItem(line="1;2;3;4;5;6")
            self.fail()

        self.assertTrue("Missing token" in str(cm.exception))

    def test_const_line_ok(self):
        expected = "1;2;3;4;5"
        m = MapFileItem(line=expected)
        self.assertEqual(1, m.Id)
        self.assertEqual("2", m.NameSpace)
        self.assertEqual("3", m.FunctionName)
        self.assertEqual("4", m.FileName)
        self.assertEqual(5, m.Line)

        self.assertEqual(expected, m.GetMapFileLine())


class TestMapFile(TestCase):
    def test_GetFilename_def(self):
        m = MapFile()
        self.assertEqual(os.path.normpath("./"+config.MAPFILE_NAME), m.GetFilename())

    def test_GetFilename_withdir(self):
        m = MapFile("test")
        self.assertEqual(os.path.normpath("test/"+config.MAPFILE_NAME), m.GetFilename())

    def saveMapFile(self, _dir, filename=None):
        i1 = MapFileItem("1;c1;f1;n1;1")
        i2 = MapFileItem("2;c2;f2;n2;2")
        i3 = MapFileItem("3;c3;f3;n3;3")
        m = MapFile(_dir)
        m.ProjectRootDir = "test/tmp"
        m.AddItems([i1, i2, i3])
        if filename is not None:
            filename = _dir + '/' + filename
        m.SaveMapFile(filename)

    def test_SaveMapFile(self):
        self.saveMapFile("test")
        m = MapFile("test")
        with open(m.GetFilename()) as f:
            lines = f.read().splitlines()
            self.assertEqual(4, len(lines))
            self.assertEqual("test/tmp", lines[0])
            self.assertEqual("1;c1;f1;n1;1", lines[1])
            self.assertEqual("2;c2;f2;n2;2", lines[2])
            self.assertEqual("3;c3;f3;n3;3", lines[3])

    def test_SaveMapFile_withName(self):
        self.saveMapFile("test", "testmap.ppmmap")
        MapFile("test")
        with open("test/testmap.ppmmap") as f:
            lines = f.read().splitlines()
            self.assertEqual(4, len(lines))
            self.assertEqual("test/tmp", lines[0])
            self.assertEqual("1;c1;f1;n1;1", lines[1])
            self.assertEqual("2;c2;f2;n2;2", lines[2])
            self.assertEqual("3;c3;f3;n3;3", lines[3])

    def test_LoadMapFile_woparam(self):
        m = MapFile("test")
        m.LoadMapFile()
        self.assertEqual(3, m.getItemsCount())

    def test_LoadMapFile_withName(self):
        self.saveMapFile("test", "testmap.ppmmap")
        m = MapFile("test")
        m.LoadMapFile(filename="test/testmap.ppmmap")
        self.assertEqual(m.ProjectRootDir, "test/tmp")
        self.assertEqual(3, m.getItemsCount())
        self.assertEqual("1;c1;f1;n1;1", m.getItem(0).GetMapFileLine())
        self.assertEqual("2;c2;f2;n2;2", m.getItem(1).GetMapFileLine())
        self.assertEqual("3;c3;f3;n3;3", m.getItem(2).GetMapFileLine())

    def test_GetMapFileItem(self):
        self.saveMapFile("test")
        m = MapFile("test")
        m.LoadMapFile()
        i = m.GetMapFileItem(2)
        self.assertEqual(m.ProjectRootDir, "test/tmp")
        self.assertEqual(3, m.getItemsCount())
        self.assertEqual(2, i.Id)

    def testAddNEwMapFileItem(self):
        MapFileItem.setStartId(100)
        m = MapFile("test")
        _id = m.AddNewMapFileItem('filename', 1000, 'namespace', 'functionname')
        self.assertEqual(1, m.getItemsCount())
        i = m.GetMapFileItem(_id)
        self.assertEqual(100+1, i.Id)
        self.assertEqual("namespace", i.NameSpace)
        self.assertEqual("functionname", i.FunctionName)
        self.assertEqual("filename", i.FileName)
        self.assertEqual(1000, i.Line)
