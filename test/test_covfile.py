from unittest import TestCase
from statfile.covfile import CovFile
from mapfile.fileinfo import File, FileInfo


class TestCovFile(TestCase):
    def test_constr(self):
        cov = CovFile(100)
        self.assertEqual(100, cov.GetCovCount())

    def test_LoadFile(self):
        filename = "test/covfile.cov"
        _str = "id;cnt\n101;1\n102;2\n103;3\n"
        File.WriteAllText(filename, _str)
        cov = CovFile(110)
        cov.LoadFile(FileInfo(filename))
        self.assertEqual(1, cov.cov[101])
        self.assertEqual(2, cov.cov[102])
        self.assertEqual(3, cov.cov[103])
