from unittest import TestCase
from mapfile.fileinfo import File, FileInfo
from mapfile.mapfile import MapFile, MapFileItem
from statfile.covfile import CovFile
from statfile.statfile import StatNode, StatData, StatFunc


class TestStatNode(TestCase):
    def test_contr_wo_param(self):
        n = StatNode()
        self.assertEqual(0, n.Count)
        self.assertEqual(0, n.Used)
        self.assertEqual(0, n.Unused)

    def test_contr_W_Param(self):
        n = StatNode(12)
        self.assertEqual(12, n.Count)
        self.assertEqual(0, n.Used)
        self.assertEqual(12, n.Unused)

    def test_set_count(self):
        n = StatNode()
        n.Count = 23
        self.assertEqual(23, n.Count)
        self.assertEqual(0, n.Used)
        self.assertEqual(23, n.Unused)

    def test_set_used(self):
        n = StatNode(12)
        n.Used = 1
        self.assertEqual(12, n.Count)
        self.assertEqual(1, n.Used)
        self.assertEqual(11, n.Unused)

    def test_AddCount(self):
        n = StatNode()
        n.AddCount(23)
        self.assertEqual(23, n.Count)
        self.assertEqual(0, n.Used)
        self.assertEqual(23, n.Unused)

    def test_AddUsed(self):
        n = StatNode(12)
        n.AddUsed(1)
        self.assertEqual(12, n.Count)
        self.assertEqual(1, n.Used)
        self.assertEqual(11, n.Unused)


class MockStatfile(object):
    def saveMapFile(self, _dir, filename=None):
        i1 = MapFileItem("101;c1;f1;test\\tmp\\n1;1")
        i2 = MapFileItem("102;c2;f2;test\\tmp\\n2;2")
        i3 = MapFileItem("103;c3;f3;test\\tmp\\n3;3")
        i4 = MapFileItem("104;c4;f4;test\\tmp\\n4;4")
        m = MapFile(_dir)
        m.ProjectRootDir = "test"
        m.AddItems([i1, i2, i3, i4])
        if filename is not None:
            filename = _dir + '/' + filename
        m.SaveMapFile(filename)


class TestStatFile(TestCase):
    def test_constr(self):
        s = StatData()
        self.assertEqual(0, len(s.stat))

    def test_CreateStat(self):
        MockStatfile().saveMapFile("test")
        m = MapFile("test")
        m.LoadMapFile()
        s = StatData()
        s.CollectMap(m)
        self.assertEqual(5, len(s.stat))

    def test_CollectUsed(self):
        MockStatfile().saveMapFile("test")
        m = MapFile("test")
        m.LoadMapFile()

        filename = "test/covfile.cov"
        _str = "id;cnt\n101;1\n102;2\n103;3\n"
        File.WriteAllText(filename, _str)
        cov = CovFile(110)
        cov.LoadFile(FileInfo(filename))

        s = StatData()
        s.CollectMap(m)
        s.CollectUsed(m, cov.getCovItems())

        self.assertEqual(3, s.stat['tmp'].Used)
        self.assertEqual(1, s.stat['tmp'].Unused)

    def test_CreateCSV(self):
        MockStatfile().saveMapFile("test")
        m = MapFile("test")
        m.LoadMapFile()

        filename = "test/covfile.cov"
        _str = "id;cnt\n101;1\n102;2\n103;3\n"
        File.WriteAllText(filename, _str)
        cov = CovFile(110)
        cov.LoadFile(FileInfo(filename))

        s = StatData()
        csv = s.CreateCSV(m, cov.getCovItems())
        _str = csv.ToString()
        exp = 'method_count;used_method_count;unused_method_count;used_method_percent;unused_method_percent;path\n4;3;1;75.00%;25.00%;tmp\n1;1;0;100.00%;0.00%;tmp\\n1\n1;1;0;100.00%;0.00%;tmp\\n2\n1;1;0;100.00%;0.00%;tmp\\n3\n1;0;1;0.00%;100.00%;tmp\\n4\n'
        self.assertEqual(exp, _str)


class TestStatFunc(TestCase):
    def test_CreateCSV(self):
        MockStatfile().saveMapFile("test")
        m = MapFile("test")
        m.LoadMapFile()

        filename = "test/covfile.cov"
        _str = "id;cnt\n101;1\n102;2\n103;3\n"
        File.WriteAllText(filename, _str)
        cov = CovFile(110)
        cov.LoadFile(FileInfo(filename))

        s = StatFunc()
        csv = s.CreateCSV(m, cov.getCovItems())
        _str = csv.ToString()
        exp = "method_id;class_name;method_name;source_file;line_num;count\n101;c1;f1;test\\tmp\\n1;1;1\n102;c2;f2;test\\tmp\\n2;2;2\n103;c3;f3;test\\tmp\\n3;3;3\n104;c4;f4;test\\tmp\\n4;4;0\n"
        self.assertEqual(exp, _str)
