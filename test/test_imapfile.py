from unittest import TestCase
from mapfile.imapfile import IMapFileItem, IMapFile
import os


class TestIMapFileItem(TestCase):
    def test_static(self):
        self.assertEqual(IMapFileItem.USERDEF_MACRO_ID, IMapFileItem.getStartId())
        IMapFileItem.setStartId(110+1)
        self.assertEqual(110+1, IMapFileItem.getStartId())
        self.assertEqual(110+2, IMapFileItem.getNextId())

    def test_const(self):
        m = IMapFileItem()
        self.assertEqual(0, m.Id)
        self.assertEqual("", m.NameSpace)
        self.assertEqual("", m.FileName)
        self.assertEqual("", m.FunctionName)
        self.assertEqual(0, m.Line)

    def test_setId(self):
        expected = 5
        m = IMapFileItem()
        m.Id = expected
        self.assertEqual(expected, m.Id)

    def test_setNameSpace(self):
        expected = "namespace"
        m = IMapFileItem()
        m.NameSpace = expected
        self.assertEqual(expected, m.NameSpace)

    def test_setFilename(self):
        expected = "filename"
        m = IMapFileItem()
        m.FileName = expected
        self.assertEqual(expected, m.FileName)

    def test_setFunctionName(self):
        expected = "funcname"
        m = IMapFileItem()
        m.FunctionName = expected
        self.assertEqual(expected, m.FunctionName)

    def test_setLine(self):
        expected = 5
        m = IMapFileItem()
        m.Line = expected
        self.assertEqual(expected, m.Line)

    def test_GetFileNameWithLine_wo_FileName(self):
        expected = ""
        m = IMapFileItem()
        result = m.GetFileNameWithLine()
        self.assertEqual(expected, result)

    def test_GetFileNameWithLine(self):
        expected = "filename ln 100"
        m = IMapFileItem()
        m.FileName = "filename"
        m.Line = 100
        result = m.GetFileNameWithLine()
        self.assertEqual(expected, result)

    def test_str_wo_function(self):
        expected = "111"
        m = IMapFileItem()
        m.Id = 111
        result = str(m)
        self.assertEqual(expected, result)

    def test_str_wo_function_user(self):
        expected = "11_user_defined_macro"
        m = IMapFileItem()
        m.Id = 11
        result = str(m)
        self.assertEqual(expected, result)

    def test_str_function(self):
        expected = "function"
        m = IMapFileItem()
        m.FunctionName = "function"
        result = str(m)
        self.assertEqual(expected, result)

    def test_str_namespace(self):
        expected = "namespace::function"
        m = IMapFileItem()
        m.NameSpace = "namespace"
        m.FunctionName = "function"
        result = str(m)
        self.assertEqual(expected, result)


class TestIMapfile(TestCase):
    def test_const(self):
        m = IMapFile()
        self.assertEqual("", m.ProjectRootDir)
        self.assertEqual(0, m.getItemsCount())

    def test_ProjectRootDir(self):
        m = IMapFile()
        m.ProjectRootDir = "root"
        self.assertEqual("root", m.ProjectRootDir)

    def test_AddItem(self):
        m = IMapFile()
        i = IMapFileItem()
        m.AddItems(i)
        self.assertEqual(1, m.getItemsCount())

    def test_AddItemList(self):
        m = IMapFile()
        items = [IMapFileItem(), IMapFileItem(), IMapFileItem()]
        m.AddItems(items)
        self.assertEqual(len(items), m.getItemsCount())

    def test_ClearItems(self):
        m = IMapFile()
        i = IMapFileItem()
        m.AddItems(i)
        m.ClearItems()
        self.assertEqual(0, m.getItemsCount())

    def test_getItem_InvalidIndex(self):
        with self.assertRaises(Exception) as cm:
            m = IMapFile()
            m.AddItems(IMapFileItem())
            m.getItem(12)
            self.fail()

        self.assertTrue("Invalid itemindex" in str(cm.exception))

    def test_getItem(self):
        i1 = IMapFileItem()
        i2 = IMapFileItem()
        i3 = IMapFileItem()
        i1.Id = 1111
        i2.Id = 2222
        i3.Id = 3333
        m = IMapFile()
        m.AddItems([i1, i2, i3])
        self.assertEqual(2222, m.getItem(1).Id)

    def test_GetLastId(self):
        i1 = IMapFileItem()
        i2 = IMapFileItem()
        i3 = IMapFileItem()
        i1.Id = 1111
        i2.Id = 2222
        i3.Id = 3333
        m = IMapFile()
        m.AddItems([i1, i2, i3])
        self.assertEqual(3333, m.GetLastId())

    def test_GetGroupName_InvalidLevel(self):
        with self.assertRaises(Exception) as cm:
            m = IMapFile()
            m.GetGroupName(IMapFileItem(), 0)
            self.fail()

        self.assertTrue("Invalid Grouplevel" in str(cm.exception))

    def test_GetGroupName_ClassLevel(self):
        i = IMapFileItem()
        i.NameSpace = 'class'
        m = IMapFile()
        m.AddItems(i)
        self.assertEqual('class', m.GetGroupName(i, IMapFile.GROUP_LEVEL_CLASS))

    def test_GetGroupName_FileLevel(self):
        i = IMapFileItem()
        i.FileName = 'file'
        m = IMapFile()
        m.AddItems(i)
        self.assertEqual('file', m.GetGroupName(i, IMapFile.GROUP_LEVEL_FILE))

    def test_GetGroupName_ModuleLevel(self):
        i = IMapFileItem()
        i.FileName = os.path.normpath("test/tmp/sub1/file3")
        m = IMapFile()
        m.ProjectRootDir = os.path.normpath("test")
        m.AddItems(i)
        self.assertEqual(os.path.normpath('tmp'), m.GetGroupName(i, IMapFile.GROUP_LEVEL_MODULE))
        self.assertEqual(os.path.normpath('tmp/sub1'), m.GetGroupName(i, IMapFile.GROUP_LEVEL_MODULE + 1))
        self.assertEqual(os.path.normpath('tmp/sub1/file3'), m.GetGroupName(i, IMapFile.GROUP_LEVEL_MODULE + 2))
        self.assertEqual('', m.GetGroupName(i, IMapFile.GROUP_LEVEL_MODULE + 3))

    def test_GetMapFileItem_EmptyItems(self):
        with self.assertRaises(Exception) as cm:
            m = IMapFile()
            m.GetMapFileItem(456)
            self.fail()

        self.assertTrue("Empty items" in str(cm.exception))

    def test_GetMapFileItem_InvalidId(self):
        with self.assertRaises(Exception) as cm:
            i = IMapFileItem()
            i.FileName = 'file'
            i.Id = 234
            m = IMapFile()
            m.AddItems(i)
            m.GetMapFileItem(456)
            self.fail()

        self.assertTrue("Invalid item id" in str(cm.exception))

    def test_GetMapFileItem(self):
        i1 = IMapFileItem()
        i1.FileName = 'file'
        i1.Id = 234
        i2 = IMapFileItem()
        i2.FileName = 'file'
        i2.Id = 235
        i3 = IMapFileItem()
        i3.FileName = 'file'
        i3.Id = 236

        m = IMapFile()
        m.AddItems([i1, i2, i3])

        # get first
        ret = m.GetMapFileItem(234)
        self.assertEqual(i1.FileName, ret.FileName)
        self.assertEqual(i1.Id, ret.Id)
        # get last
        ret = m.GetMapFileItem(236)
        self.assertEqual(i3.FileName, ret.FileName)
        self.assertEqual(i3.Id, ret.Id)
        # get middle
        ret = m.GetMapFileItem(235)
        self.assertEqual(i2.FileName, ret.FileName)
        self.assertEqual(i2.Id, ret.Id)
