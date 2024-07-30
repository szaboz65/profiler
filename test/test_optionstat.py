from unittest import TestCase
from appstat.optionstat import OptionStat


class TestOptionStat(TestCase):
    def test_const(self):
        o = OptionStat()
        self.assertFalse(o.isDebug)
        self.assertFalse(o.isVerbose)
        self.assertFalse(o.isLog)
        self.assertEqual(".", o.ParseDir)
        self.assertEqual(".", o.OutputDir)
        self.assertEqual("", o.MapFileName)

    def test_loadOptions_debug(self):
        o = OptionStat()
        error = o.loadOptions("test", ["-d"])
        self.assertEqual(OptionStat.OK, error)
        self.assertTrue(o.isDebug)

    def test_loadOptions_debug2(self):
        o = OptionStat()
        error = o.loadOptions("test", ["--debug"])
        self.assertEqual(OptionStat.OK, error)
        self.assertTrue(o.isDebug)

    def test_loadOptions_verbose(self):
        o = OptionStat()
        error = o.loadOptions("test", ["-b"])
        self.assertEqual(OptionStat.OK, error)
        self.assertTrue(o.isVerbose)

    def test_loadOptions_verbose2(self):
        o = OptionStat()
        error = o.loadOptions("test", ["--verbose"])
        self.assertEqual(OptionStat.OK, error)
        self.assertTrue(o.isVerbose)

    def test_loadOptions_log(self):
        o = OptionStat()
        error = o.loadOptions("test", ["-l"])
        self.assertEqual(OptionStat.OK, error)
        self.assertTrue(o.isLog)

    def test_loadOptions_log2(self):
        o = OptionStat()
        error = o.loadOptions("test", ["--log"])
        self.assertEqual(OptionStat.OK, error)
        self.assertTrue(o.isLog)

    def test_loadOptions_help(self):
        o = OptionStat()
        error = o.loadOptions("test", ["-h"])
        self.assertEqual(OptionStat.EXIT, error)

    def test_loadOptions_help2(self):
        o = OptionStat()
        error = o.loadOptions("test", ["--help"])
        self.assertEqual(OptionStat.EXIT, error)

    def test_loadOptions_version(self):
        o = OptionStat()
        error = o.loadOptions("test", ["-v"])
        self.assertEqual(OptionStat.EXIT, error)

    def test_loadOptions_version2(self):
        o = OptionStat()
        error = o.loadOptions("test", ["--version"])
        self.assertEqual(OptionStat.EXIT, error)

    def test_loadOptions_parsedir(self):
        _dir = "test/tmp/dir1"
        o = OptionStat()
        error = o.loadOptions("test", [_dir])
        self.assertEqual(OptionStat.OK, error)
        self.assertEqual(_dir, o.ParseDir)

    def test_loadOptions_mapfilename(self):
        _dir = "test/tmp/dir1"
        fname = "test/mapfilename"
        o = OptionStat()
        error = o.loadOptions("test", [_dir, fname])
        self.assertEqual(OptionStat.OK, error)
        self.assertEqual(_dir, o.ParseDir)
        self.assertEqual(fname, o.MapFileName)

    def test_loadOptions_outdir(self):
        o = OptionStat()
        error = o.loadOptions("test", ["-otest"])
        self.assertEqual(OptionStat.OK, error)
        self.assertEqual("test", o.OutputDir)

    def test_loadOptions_outdir2(self):
        o = OptionStat()
        error = o.loadOptions("test", ["--outdir=test"])
        self.assertEqual(OptionStat.OK, error)
        self.assertEqual("test", o.OutputDir)
