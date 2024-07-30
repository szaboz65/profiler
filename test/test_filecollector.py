from unittest import TestCase
from mapfile.filecollector import FileCollector
from mapfile.fileinfo import FileInfo, DirectoryInfo


class TestFileCollector(TestCase):
    def test_const(self):
        p = FileCollector()
        self.assertEqual(0, p.GetFilesCount())

    def test_AddFiles_only_one(self):
        p = FileCollector()
        file = FileInfo("test/tmp/file1")
        p.AddFiles(file)
        self.assertEqual(1, p.GetFilesCount())
        self.assertEqual(file.FullName, p.Files[0].FullName)

    def test_AddFiles_list(self):
        p = FileCollector()
        file1 = FileInfo("test/tmp/file1")
        file2 = FileInfo("test/tmp/file2")
        p.AddFiles([file1, file2])
        self.assertEqual(2, p.GetFilesCount())
        self.assertEqual(file2.FullName, p.Files[1].FullName)

    def test_ClearFiles(self):
        p = FileCollector()
        file = FileInfo("test/tmp/file1")
        p.AddFiles(file)
        p.ClearFiles()
        self.assertEqual(0, p.GetFilesCount())

    def test_IsExcludeDir(self):
        p = FileCollector()
        dirs = DirectoryInfo('./test/tmp').GetDirectories()
        self.assertFalse(p.IsExcludeDir(dirs[0].Name))
        p.AddExcludeDir(dirs[0].Name)
        self.assertTrue(p.IsExcludeDir(dirs[0].Name))
        p.AddExcludeDir([d.Name for d in dirs])
        self.assertTrue(p.IsExcludeDir(dirs[1].Name))

    def test_IsExcludeFile(self):
        p = FileCollector()
        files = DirectoryInfo('./test/tmp').GetFiles()
        self.assertFalse(p.IsExcludeFile(files[0].FullName))
        p.AddExcludeFile(files[0].FullName)
        self.assertTrue(p.IsExcludeFile(files[0].FullName))
        p.AddExcludeFile([f.FullName for f in files])
        self.assertTrue(p.IsExcludeFile(files[1].FullName))

    def test_IsExcludeFile_byfile(self):
        p = FileCollector()
        files = ['test/tmp/file1', 'test/tmp/file2']
        self.assertFalse(p.IsExcludeFile(files[0]))
        p.AddExcludeFile(files[0])
        self.assertTrue(p.IsExcludeFile(files[0]))
        p.AddExcludeFile([f for f in files])
        self.assertTrue(p.IsExcludeFile(files[1]))

    def test_AddDirectory(self):
        _dir = DirectoryInfo('./test/tmp')
        p = FileCollector()
        p.AddDirectory(_dir)
        self.assertEqual(6, p.GetFilesCount())

    def test_CollectDirs_only_one(self):
        m = FileCollector()
        m.CollectDirs('./test/tmp/sub1')
        self.assertEqual(2, m.GetFilesCount())

    def test_CollectDirs_list(self):
        m = FileCollector()
        m.CollectDirs(['./test/tmp/sub1', './test/tmp/sub2'])
        self.assertEqual(4, m.GetFilesCount())

    def test_CollectDirs_recursively(self):
        m = FileCollector()
        m.CollectDirs('./test/tmp')
        self.assertEqual(6, m.GetFilesCount())

    def test_CollectFiles_only_one(self):
        m = FileCollector()
        m.CollectFiles('test/tmp/file1')
        self.assertEqual(1, m.GetFilesCount())

    def test_CollectFiles_list(self):
        m = FileCollector()
        m.CollectFiles(['test/tmp/file1', 'test/tmp/file2'])
        self.assertEqual(2, m.GetFilesCount())

    def test_CollectDirs_with_exclusedir(self):
        m = FileCollector(excludeDirs=['test/tmp/sub1'])
        m.CollectDirs('./test/tmp')
        self.assertEqual(4, m.GetFilesCount())

    def test_CollectDirs_with_exclusefile(self):
        m = FileCollector(excludeFiles=['test/tmp/file1'])
        m.CollectDirs('./test/tmp')
        self.assertEqual(5, m.GetFilesCount())
