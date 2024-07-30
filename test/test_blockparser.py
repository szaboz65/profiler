from unittest import TestCase
from parser.blockparserbase import BlockParserBase
from parser.iblock import BlockType


class MockBlock(object):
    def __init__(self, parent, _str, iStart, iEnd, _type=BlockType.UNKNOWN):
        self.m_str = _str
        self.m_iStart = iStart
        self.m_iEnd = iEnd
        self.m_Parent = parent
        self.m_Type = _type


class MyBlockParser(BlockParserBase):
    def __init__(self, strText, mtype):
        BlockParserBase.__init__(self, strText)
        self.type = mtype

    def CreateBlock(self, parent, iStart, iEnd):
        block = MockBlock(parent, 'str', iStart, iEnd, self.type)
        if self.type == BlockType.NAMESPACE:
            self.type = BlockType.FUNCTION
        return block


class TestBlockParser(TestCase):
    def test_constr(self):
        strText = "asdfg"
        p = BlockParserBase(strText)
        self.assertEqual(strText, p.strText)
        self.assertEqual(0, p.index)

    def test_IsFalseQuotation_empty(self):
        strText = ""
        p = BlockParserBase(strText)
        self.assertFalse(p.IsFalseQuotation())

    def test_IsFalseQuotation_ch1(self):
        strText = "\'a\'"
        p = BlockParserBase(strText)
        p.index = 1
        self.assertTrue(p.IsFalseQuotation())

    def test_IsFalseQuotation_ch2(self):
        strText = "txt\\\""
        p = BlockParserBase(strText)
        p.index = len(strText)-1
        self.assertTrue(p.IsFalseQuotation())

    def test_IsFalseQuotation_ch3(self):
        strText = "txt\\"
        p = BlockParserBase(strText)
        p.index = len(strText)-1
        self.assertFalse(p.IsFalseQuotation())

    def test_SkipQuotation(self):
        strText = "\"a\"next"
        p = BlockParserBase(strText)
        p.index = 1
        p.SkipQuotation()
        self.assertEqual(strText.find('n'), p.index)

    def test_SkipQuotation2(self):
        strText = "\"a\\\"\"next"
        p = BlockParserBase(strText)
        p.index = 1
        p.SkipQuotation()
        self.assertEqual(strText.find('n'), p.index)

    def test_FindNextLine(self):
        strText = "elso\nmasodik\nnext"
        p = BlockParserBase(strText)
        p.FindNextLine()
        self.assertEqual(strText.find('m'), p.index)

    def test_FindNextLine2(self):
        strText = "elso masodik next"
        p = BlockParserBase(strText)
        p.FindNextLine()
        self.assertEqual(len(strText), p.index+1)

    def test_SkipIfDef(self):
        strText = "#ifdef\nx chars\n#endif \ny"
        p = BlockParserBase(strText)
        result = p.SkipIfDef()
        self.assertTrue(result)
        self.assertEqual(strText.find('y'), p.index)

    def test_SkipIfDef_noif(self):
        strText = "#include\nx chars\n#endif \ny"
        p = BlockParserBase(strText)
        result = p.SkipIfDef()
        self.assertFalse(result)
        self.assertEqual(strText.find('#'), p.index)

    def test_SkipIfDef_double(self):
        strText = "#ifdef ss\n#endif ss\nx chars\n#if dd \n#endif // dd\ny"
        p = BlockParserBase(strText)
        result = p.SkipIfDef()
        self.assertTrue(result)
        self.assertEqual(strText.find('x'), p.index)

    def test_SkipIfDef_nested(self):
        strText = "#ifdef ss\n#if dd\nx chars\n#endif //dd \n#endif // ss\ny"
        p = BlockParserBase(strText)
        result = p.SkipIfDef()
        self.assertTrue(result)
        self.assertEqual(strText.find('y'), p.index)

    def test_SkipIfDef_missing_endif(self):
        with self.assertRaises(Exception) as cm:
            strText = "#ifdef\nx chars\n#end \ny"
            p = BlockParserBase(strText)
            p.SkipIfDef()
            self.fail()
        self.assertTrue("Missing #endif" in str(cm.exception))

    def test_SkipIfDef_nested_missing_endif(self):
        with self.assertRaises(Exception) as cm:
            strText = "#ifdef ss\n#if dd\nx chars\n#endif //dd \n#end // ss\ny"
            p = BlockParserBase(strText)
            p.SkipIfDef()
            self.fail()
        self.assertTrue("Missing #endif" in str(cm.exception))

    def test_SkipIfNeed_comment(self):
        strText = "// comment\nx chars\n"
        p = BlockParserBase(strText)
        result = p.SkipIfNeed()
        self.assertTrue(result)
        self.assertEqual(strText.find('x'), p.index)

    def test_SkipIfNeed_Quotation(self):
        strText = "\"adat\"x chars\n"
        p = BlockParserBase(strText)
        result = p.SkipIfNeed()
        self.assertTrue(result)
        self.assertEqual(strText.find('x'), p.index)

    def test_SkipIfNeed_remark(self):
        strText = "/*ada*t/\" a sorban*/x chars\n"
        p = BlockParserBase(strText)
        result = p.SkipIfNeed()
        self.assertTrue(result)
        self.assertEqual(strText.find('x'), p.index)

    def test_SkipIfNeed_illegalremark(self):
        with self.assertRaises(Exception) as cm:
            strText = "/*ada*t/\" a sorban*-/x chars\n"
            p = BlockParserBase(strText)
            p.SkipIfNeed()
            self.fail()
        self.assertTrue("Outstanding comment" in str(cm.exception))

    def test_SkipIfNeed_preprocess(self):
        strText = "#include ssdd\nx"
        p = BlockParserBase(strText)
        result = p.SkipIfNeed()
        self.assertTrue(result)
        self.assertEqual(strText.find('x'), p.index)

    def test_SkipIfNeed_define(self):
        strText = "#define ssdd\\\\\n second line\\\\third line\nx"
        p = BlockParserBase(strText)
        result = p.SkipIfNeed()
        self.assertTrue(result)
        self.assertEqual(strText.find('x'), p.index)

    def test_SkipIfNeed_noskip(self):
        strText = "A define ssdd\\\\\n second line\\\\third line\nx"
        p = BlockParserBase(strText)
        result = p.SkipIfNeed()
        self.assertFalse(result)
        self.assertEqual(strText.find('A'), p.index)

    def test_GetNextBlock_noblock(self):
        strText = "A define ssdd\\\\\n second line\\\\third line\nx"
        p = BlockParserBase(strText)
        result = p.GetNextBlock(None)
        self.assertIsNone(result)

    def test_GetNextBlock_noclose(self):
        strText = "A define ssdd\\\\\n{ second line\\\\\nthird line\nx"
        p = BlockParserBase(strText)
        result = p.GetNextBlock(None)
        self.assertIsNone(result)

    def test_GetNextBlock_noopen(self):
        strText = "A define ssdd\\\\\n second line\\\\\nthird line}\nx"
        p = BlockParserBase(strText)
        result = p.GetNextBlock(None)
        self.assertIsNone(result)

    def makeBlockParser(self, strText, btype=BlockType.UNKNOWN):
        return MyBlockParser(strText, btype)

    def test_GetNextBlock_ok(self):
        strText = "A define ssdd\\\\\n { second line\nthird line\n}\nx"
        p = self.makeBlockParser(strText)
        result = p.GetNextBlock(None)
        self.assertIsNotNone(result)
        self.assertEqual("{ second line\nthird line\n}", strText[result.m_iStart: result.m_iEnd])

    def test_GetNextBlock_nested_ok(self):
        strText = "A define ssdd\\\\\n { second line\nif(1) { third line }\n}\nx"
        p = self.makeBlockParser(strText)
        result = p.GetNextBlock(None)
        self.assertIsNotNone(result)
        self.assertEqual("{ second line\nif(1) { third line }\n}", strText[result.m_iStart: result.m_iEnd])

    def test_GetBlocks_none(self):
        strText = "A define ssdd\\\\\n  second line\nthird line\n\nx"
        p = self.makeBlockParser(strText)
        result = p.GetBlocks()
        self.assertEqual(0, len(result))

    def test_GetBlocks_unknown(self):
        strText = "A define ssdd\n{  second line\nthird line\n}\nx"
        p = self.makeBlockParser(strText)
        result = p.GetBlocks()
        self.assertEqual(0, len(result))

    def test_GetBlocks_function(self):
        strText = "A function (ssdd)\n{  second line\nthird line\n}\nx"
        p = self.makeBlockParser(strText, BlockType.FUNCTION)
        result = p.GetBlocks()
        self.assertEqual(1, len(result))

    def test_GetBlocks_namespace_only(self):
        strText = "A namespace (ssdd)\n{  second line\nthird line\n}\nx"
        p = self.makeBlockParser(strText, BlockType.NAMESPACE)
        result = p.GetBlocks()
        self.assertEqual(1, len(result))

    def test_GetBlocks_namespace_one_func(self):
        strText = "A namespace (ssdd)\n{  function n(j)\n{\nsecond line\nthird line\n}}\nx"
        p = self.makeBlockParser(strText, BlockType.NAMESPACE)
        result = p.GetBlocks()
        self.assertEqual(2, len(result))
        self.assertEqual(result[1].m_Parent, result[0])

    def test_GetBlocks_namespace_two_func(self):
        strText = "A namespace (ssdd)\n{  function n(j)\n{\nsecond line\nthird line\n}\n func(d){lines}}\nx"
        p = self.makeBlockParser(strText, BlockType.NAMESPACE)
        result = p.GetBlocks()
        self.assertEqual(3, len(result))
        self.assertEqual(result[1].m_Parent, result[0])
        self.assertEqual(result[2].m_Parent, result[0])

    def test_GetBlocks_namespace_func_block(self):
        strText = "A namespace (ssdd)\n{  function n(j)\n{\nsecond line\nthird line\n}\n if(g) {lines}}\nx"
        p = self.makeBlockParser(strText, BlockType.NAMESPACE)
        result = p.GetBlocks()
        self.assertEqual(3, len(result))
        self.assertEqual(result[1].m_Parent, result[0])
        self.assertEqual(result[2].m_Parent, result[0])
