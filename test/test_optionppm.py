from unittest import TestCase
from appppm.optionppm import OptionPPM


class TestOptionPPM(TestCase):
    def test_const(self):
        o = OptionPPM()
        self.assertFalse(o.isDebug)
        self.assertFalse(o.isVerbose)
        self.assertFalse(o.isLog)
        self.assertFalse(o.isCoding)
        self.assertFalse(o.isClear)
        self.assertEqual(".", o.ProjectRootDir)
        self.assertEqual(".", o.MapFileDir)
        self.assertEqual([], o.ExcludeDirs)
        self.assertEqual([], o.ExcludeFiles)
        self.assertEqual([], o.ParseDirs)
        self.assertEqual([], o.ParseFiles)

    def test_loadOptions_debug(self):
        o = OptionPPM()
        error = o.loadOptions("test", ["-d"])
        self.assertEqual(OptionPPM.OK, error)
        self.assertTrue(o.isDebug)

    def test_loadOptions_debug2(self):
        o = OptionPPM()
        error = o.loadOptions("test", ["--debug"])
        self.assertEqual(OptionPPM.OK, error)
        self.assertTrue(o.isDebug)

    def test_loadOptions_verbose(self):
        o = OptionPPM()
        error = o.loadOptions("test", ["-b"])
        self.assertEqual(OptionPPM.OK, error)
        self.assertTrue(o.isVerbose)

    def test_loadOptions_verbose2(self):
        o = OptionPPM()
        error = o.loadOptions("test", ["--verbose"])
        self.assertEqual(OptionPPM.OK, error)
        self.assertTrue(o.isVerbose)

    def test_loadOptions_clear(self):
        o = OptionPPM()
        error = o.loadOptions("test", ["-c"])
        self.assertEqual(OptionPPM.OK, error)
        self.assertTrue(o.isClear)

    def test_loadOptions_clear2(self):
        o = OptionPPM()
        error = o.loadOptions("test", ["--clear"])
        self.assertEqual(OptionPPM.OK, error)
        self.assertTrue(o.isClear)

    def test_loadOptions_autocoding(self):
        o = OptionPPM()
        error = o.loadOptions("test", ["-a"])
        self.assertEqual(OptionPPM.OK, error)
        self.assertTrue(o.isCoding)

    def test_loadOptions_autocoding2(self):
        o = OptionPPM()
        error = o.loadOptions("test", ["--autocoding"])
        self.assertEqual(OptionPPM.OK, error)
        self.assertTrue(o.isCoding)

    def test_loadOptions_log(self):
        o = OptionPPM()
        error = o.loadOptions("test", ["-l"])
        self.assertEqual(OptionPPM.OK, error)
        self.assertTrue(o.isLog)

    def test_loadOptions_log2(self):
        o = OptionPPM()
        error = o.loadOptions("test", ["--log"])
        self.assertEqual(OptionPPM.OK, error)
        self.assertTrue(o.isLog)

    def test_loadOptions_help(self):
        o = OptionPPM()
        error = o.loadOptions("test", ["-h"])
        self.assertEqual(OptionPPM.EXIT, error)

    def test_loadOptions_help2(self):
        o = OptionPPM()
        error = o.loadOptions("test", ["--help"])
        self.assertEqual(OptionPPM.EXIT, error)

    def test_loadOptions_version(self):
        o = OptionPPM()
        error = o.loadOptions("test", ["-v"])
        self.assertEqual(OptionPPM.EXIT, error)

    def test_loadOptions_version2(self):
        o = OptionPPM()
        error = o.loadOptions("test", ["--version"])
        self.assertEqual(OptionPPM.EXIT, error)

    def test_loadOptions_parse(self):
        _dir = "test/tmp/dir1"
        o = OptionPPM()
        error = o.loadOptions("test", ["-p"+_dir])
        self.assertEqual(OptionPPM.OK, error)
        self.assertEqual([_dir], o.ParseDirs)

    def test_loadOptions_parse2(self):
        _dir = "test/tmp/dir1"
        o = OptionPPM()
        error = o.loadOptions("test", ["--parse="+_dir])
        self.assertEqual(OptionPPM.OK, error)
        self.assertEqual([_dir], o.ParseDirs)

    def test_loadOptions_mapdir(self):
        _dir = "test"
        o = OptionPPM()
        error = o.loadOptions("test", ["-m"+_dir])
        self.assertEqual(OptionPPM.OK, error)
        self.assertEqual(_dir, o.MapFileDir)

    def test_loadOptions_mapdir2(self):
        _dir = "test"
        o = OptionPPM()
        error = o.loadOptions("test", ["--mapdir="+_dir])
        self.assertEqual(OptionPPM.OK, error)
        self.assertEqual(_dir, o.MapFileDir)

    def test_loadOptions_root(self):
        _dir = "test/tmp/dir1"
        o = OptionPPM()
        error = o.loadOptions("test", ["-r"+_dir])
        self.assertEqual(OptionPPM.OK, error)
        self.assertEqual(_dir, o.ProjectRootDir)

    def test_loadOptions_root_list(self):
        _dir = "test/tmp/dir1"
        _dir = _dir + OptionPPM.SEPARATOR + _dir
        o = OptionPPM()
        error = o.loadOptions("test", ["-r"+_dir])
        self.assertEqual(OptionPPM.OK, error)
        self.assertEqual(_dir, o.ProjectRootDir)

    def test_loadOptions_root2(self):
        _dir = "test/tmp/dir1"
        o = OptionPPM()
        error = o.loadOptions("test", ["--root="+_dir])
        self.assertEqual(OptionPPM.OK, error)
        self.assertEqual(_dir, o.ProjectRootDir)

    def test_loadOptions_root2_list(self):
        _dir = "test/tmp/dir1"
        _dir = _dir + OptionPPM.SEPARATOR + _dir
        o = OptionPPM()
        error = o.loadOptions("test", ["--root="+_dir])
        self.assertEqual(OptionPPM.OK, error)
        self.assertEqual(_dir, o.ProjectRootDir)

    def test_loadOptions_nofile(self):
        o = OptionPPM()
        error = o.loadOptions("test", [""])
        self.assertEqual(OptionPPM.OK, error)
        self.assertEqual([], o.ParseFiles)

    def test_loadOptions_one_file(self):
        o = OptionPPM()
        error = o.loadOptions("test", ["filename"])
        self.assertEqual(OptionPPM.OK, error)
        self.assertEqual(["filename"], o.ParseFiles)

    def test_loadOptions_more_file(self):
        o = OptionPPM()
        error = o.loadOptions("test", ["filename1", "filename2"])
        self.assertEqual(OptionPPM.OK, error)
        self.assertEqual(["filename1", "filename2"], o.ParseFiles)

    def test_loadOptions_files(self):
        o = OptionPPM()
        error = o.loadOptions("test", ["-xfile1;file2;file3;file4"])
        self.assertEqual(OptionPPM.OK, error)
        self.assertEqual(4, len(o.ExcludeFiles))

    def test_loadOptions_files2(self):
        o = OptionPPM()
        error = o.loadOptions("test", ["--excfile=file1;file2;file3;file4"])
        self.assertEqual(OptionPPM.OK, error)
        self.assertEqual(4, len(o.ExcludeFiles))

    def test_loadOptions_undefined(self):
        o = OptionPPM()
        error = o.loadOptions("test", ["-."])
        self.assertEqual(OptionPPM.ERROR, error)
