from unittest import TestCase
from statfile.istatfile import iCovFile


class TestICovFile(TestCase):
    def test_constr(self):
        cov = iCovFile(100)
        self.assertEqual(0, cov.cov[0])

    def test_GetCovCount(self):
        cov = iCovFile(100)
        self.assertEqual(100, cov.GetCovCount())

    def test_AddCovItem(self):
        cov = iCovFile(100)
        cov.AddCovItem(10, 100)
        self.assertEqual(100, cov.cov[10])
