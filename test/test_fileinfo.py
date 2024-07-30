from unittest import TestCase
from mapfile.fileinfo import DirectoryInfo, FileInfo, File
import os


class TestFile(TestCase):
    def test_WriteAllText(self):
        _str = "text123"
        b = File.WriteAllText("test/file.txt", _str)
        self.assertTrue(b)

    def test_Exists(self):
        self.assertTrue(File.Exists("test/file.txt"))

    def test_FileSize(self):
        self.assertTrue(len("text123"), File.FileSize("test/file.txt"))

    def test_ReadAllText(self):
        _str = "text123"
        load = File.ReadAllText("test/file.txt")
        self.assertEqual(_str, load)

    def test_ReadAllText_notexist(self):
        load = File.ReadAllText("test/__file__.txt")
        self.assertEqual("", load)

    def test_FindFile(self):
        load = File.FindFile("test", "file.txt")
        self.assertEqual(os.path.normpath("test/file.txt"), load)

    def test_FindFile_notexist(self):
        load = File.FindFile("kismano", "file.txt")
        self.assertIsNone(load)

    def test_Delete(self):
        filename = "test/file2.txt"
        File.WriteAllText(filename, "0")
        self.assertTrue(File.Exists(filename))
        File.Delete(filename)
        self.assertFalse(File.Exists(filename))


class TestFileInfo(TestCase):
    def test_get_FullName(self):
        path = "test/file.cpp"
        f = FileInfo(path)
        self.assertEqual(path, f.FullName)

    def test_get_Extension(self):
        path = "test/file.cpp"
        f = FileInfo(path)
        self.assertEqual('.cpp', f.Extension)

    def test_get_Name(self):
        path = "test/file.cpp"
        f = FileInfo(path)
        self.assertEqual('test/file', f.Name)

    def test_is_Exist(self):
        path = "test/file.cpp"
        f = FileInfo(path)
        self.assertTrue(f.Exists)

    def test_get_Size(self):
        path = "test/file.cpp"
        f = FileInfo(path)
        self.assertEqual(10, f.Length)


class TestDirectoryInfo(TestCase):
    def test_const_notexist(self):
        d = DirectoryInfo("directorynotexist")
        self.assertListEqual([], d.GetDirectories())
        self.assertListEqual([], d.GetFiles())

    def test_const_exists(self):
        def createdirs():
            os.mkdir('./test/tmp')
            os.mkdir('./test/tmp/sub1')
            os.mkdir('./test/tmp/sub2')
            open('./test/tmp/file1', 'a').close()
            open('./test/tmp/file2', 'a').close()
            open('./test/tmp/sub1/file2', 'a').close()
            open('./test/tmp/sub1/file3', 'a').close()
            open('./test/tmp/sub2/file4', 'a').close()
            open('./test/tmp/sub2/file5', 'a').close()

        if not os.path.isdir("./test/tmp"):
            createdirs()

        di = DirectoryInfo("./test/tmp")
        self.assertEqual(os.path.normpath("./test/tmp"), di.Name)

    def test_GetDirectories(self):
        di = DirectoryInfo("./test/tmp")
        result = di.GetDirectories()
        expected = [os.path.normpath('./test/tmp/sub1'), os.path.normpath('./test/tmp/sub2')]
        self.assertEqual(expected, [d.Name for d in result])

    def test_GetFiles(self):
        di = DirectoryInfo("./test/tmp")
        result = di.GetFiles()
        expected = [os.path.normpath('./test/tmp/file1'), os.path.normpath('./test/tmp/file2')]
        self.assertEqual(expected, [f.FullName for f in result])
