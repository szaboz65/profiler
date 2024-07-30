from unittest import TestCase
from parser.iblock import iBlock, BlockType


class TestIBlock(TestCase):
    def test_constr(self):
        b = iBlock()
        self.assertIsNone(None, b.m_Parent)
        self.assertEqual(BlockType.UNKNOWN, b.m_Type)
        self.assertEqual("", b.m_strNamespace)
        self.assertEqual("", b.m_strFunctionName)

    def test_GetFunctionName(self):
        b = iBlock()
        b.m_strFunctionName = "funcname"
        self.assertEqual("funcname", b.GetFunctionName())

    def test_GetNamespace(self):
        b = iBlock()
        b.m_strNamespace = "namespace"
        self.assertEqual("namespace", b.GetNamespace())

    def test_ToString_func(self):
        b = iBlock()
        b.m_strFunctionName = "name"
        self.assertEqual("name", str(b))

    def test_ToString_namespace(self):
        b = iBlock()
        b.m_strFunctionName = "name"
        b.m_strNamespace = "class"
        self.assertEqual("class::name", str(b))

    def test_GetNamespace_parent(self):
        b1 = iBlock()
        b1.m_strFunctionName = "name1"
        b1.m_strNamespace = "class1"
        b2 = iBlock(b1)
        b2.m_strFunctionName = "name2"
        b2.m_strNamespace = "class2"
        self.assertEqual("class1::class2", b2.GetNamespace())
