from unittest import TestCase
from parser.iblock import BlockType
from parser.block import Block


class TestBlock(TestCase):
    def test_constr_wo_parent(self):
        text = ""
        b = Block(None, text, 0, len(text))
        self.assertEqual(text, b.m_str)
        self.assertEqual(0, b.m_iStart)
        self.assertEqual(len(text), b.m_iEnd)
        self.assertIsNone(None, b.m_Parent)
        self.assertEqual(BlockType.UNKNOWN, b.m_Type)
        self.assertEqual("", b.m_strHeader)
        self.assertEqual("", b.m_strNamespace)
        self.assertEqual("", b.m_strFunctionName)

    def test_IsMacroBlock_insideblock(self):
        text = "macrodef\nmacroblock\\\\\nmacroend"
        iStart = text.find('\n')
        iEnd = text.rfind('\n')
        b = Block(None, text, iStart+1, iEnd)
        self.assertEqual(BlockType.MACRO, b.m_Type)
        self.assertEqual("macroblock\\\\", b.GetText())

    def test_InitNameSpace_none(self):
        strHeader = "type func"
        b = Block(None, "", 0, 0)
        ret = b.InitNamespace(strHeader)
        self.assertFalse(ret)
        self.assertEqual("", b.GetNamespace())

    def test_InitNameSpace_ok(self):
        strHeader = "namespace   \t ns"
        b = Block(None, "", 0, 0)
        ret = b.InitNamespace(strHeader)
        self.assertTrue(ret)
        self.assertEqual("ns", b.GetNamespace())

    def test_InitFuntion_nonamespace(self):
        strHeader = "type func"
        b = Block(None, "", 0, 0)
        ret = b.InitFunction(strHeader)
        self.assertTrue(ret)
        self.assertEqual("func", b.GetFunctionName())
        self.assertEqual("", b.GetNamespace())

    def test_InitFuntion_nonamespace_oneletter(self):
        strHeader = "t f"
        b = Block(None, "", 0, 0)
        ret = b.InitFunction(strHeader)
        self.assertTrue(ret)
        self.assertEqual("f", b.GetFunctionName())
        self.assertEqual("", b.GetNamespace())

    def test_InitFuntion_classfn(self):
        strHeader = "type class::func"
        b = Block(None, "", 0, 0)
        ret = b.InitFunction(strHeader)
        self.assertTrue(ret)
        self.assertEqual("func", b.GetFunctionName())
        self.assertEqual("class", b.GetNamespace())

    def test_InitFuntion_multiple_classfn(self):
        strHeader = "type class::inner::func"
        b = Block(None, "", 0, 0)
        ret = b.InitFunction(strHeader)
        self.assertTrue(ret)
        self.assertEqual("func", b.GetFunctionName())
        self.assertEqual("class::inner", b.GetNamespace())

    def test_InitFuntion_classfn_type(self):
        strHeader = "class::type class::func"
        b = Block(None, "", 0, 0)
        ret = b.InitFunction(strHeader)
        self.assertTrue(ret)
        self.assertEqual("func", b.GetFunctionName())
        self.assertEqual("class", b.GetNamespace())

    def test_InitFuntion_classconstr(self):
        strHeader = "class::constr"
        b = Block(None, "", 0, 0)
        ret = b.InitFunction(strHeader)
        self.assertTrue(ret)
        self.assertEqual("constr", b.GetFunctionName())
        self.assertEqual("class", b.GetNamespace())

    # test blocks
    def test_block_namespace(self):
        text = "\nnamespace kiskutya\n\n {\n nnext line \n};"
        iStart = text.find('{')
        iEnd = text.find('}', iStart+1)
        b = Block(None, text, iStart, iEnd)
        self.assertEqual('namespace kiskutya', b.m_strHeader)
        self.assertEqual(BlockType.NAMESPACE, b.m_Type)
        self.assertEqual('kiskutya', b.GetNamespace())

    def test_block_array(self):
        text = "\ntype xx=\n\n {\n nnext line \n};"
        iStart = text.find('{')
        iEnd = text.find('}', iStart+1)
        b = Block(None, text, iStart, iEnd)
        self.assertEqual('type xx=', b.m_strHeader)
        self.assertEqual(BlockType.ARRAY, b.m_Type)

    def test_block_union(self):
        text = "\nunion xx\n { nnext line }"
        iStart = text.find('{')
        iEnd = text.find('}', iStart+1)
        b = Block(None, text, iStart, iEnd)
        self.assertEqual('union xx', b.m_strHeader)
        self.assertEqual(BlockType.UNION, b.m_Type)

    def test_block_extern(self):
        text = "\nextern \"C\"\n { nnext line };\n"
        iStart = text.find('{')
        iEnd = text.find('}', iStart+1)
        b = Block(None, text, iStart, iEnd)
        self.assertEqual('extern \"C\"', b.m_strHeader)
        self.assertEqual(BlockType.EXTERN, b.m_Type)

    def test_block_enum(self):
        text = "\nenum eee\n {\n nnext=line\n }\n"
        iStart = text.find('{')
        iEnd = text.find('}', iStart+1)
        b = Block(None, text, iStart, iEnd)
        self.assertEqual('enum eee', b.m_strHeader)
        self.assertEqual(BlockType.ENUM, b.m_Type)

    def test_block_typedef(self):
        text = "\n typedef tte\n {\n nnext=line\n }\n"
        iStart = text.find('{')
        iEnd = text.find('}', iStart+1)
        b = Block(None, text, iStart, iEnd)
        self.assertEqual('typedef tte', b.m_strHeader)
        self.assertEqual(BlockType.TYPEDEF, b.m_Type)

    def test_block_struct(self):
        text = "\nstruct see\n {\n nnext=line\n }\n"
        iStart = text.find('{')
        iEnd = text.find('}', iStart+1)
        b = Block(None, text, iStart, iEnd)
        self.assertEqual('struct see', b.m_strHeader)
        self.assertEqual(BlockType.CLASSSTRUCT, b.m_Type)

    def test_block_class(self):
        text = "\nclass cee\n {\n nnext{line}\n }\n"
        iStart = text.find('{')
        iEnd = text.find('}', iStart+1)
        b = Block(None, text, iStart, iEnd)
        self.assertEqual('class cee', b.m_strHeader)
        self.assertEqual(BlockType.CLASSSTRUCT, b.m_Type)

    def test_block_struct_noname(self):
        text = "\nstruct\n {\n nnext=line\n }\n"
        iStart = text.find('{')
        iEnd = text.find('}', iStart+1)
        b = Block(None, text, iStart, iEnd)
        self.assertEqual('struct', b.m_strHeader)
        self.assertEqual(BlockType.CLASSSTRUCT, b.m_Type)

    def test_block_struct_name(self):
        text = "\nstruct valami\n {\n nnext=line\n }\n"
        iStart = text.find('{')
        iEnd = text.find('}', iStart+1)
        b = Block(None, text, iStart, iEnd)
        self.assertEqual('struct valami', b.m_strHeader)
        self.assertEqual(BlockType.CLASSSTRUCT, b.m_Type)

    def test_block_class_name(self):
        text = "\nclass macska\n {\n nnext{line}\n }\n"
        iStart = text.find('{')
        iEnd = text.find('}', iStart+1)
        b = Block(None, text, iStart, iEnd)
        self.assertEqual('class macska', b.m_strHeader)
        self.assertEqual(BlockType.CLASSSTRUCT, b.m_Type)

    def test_block_class_oneline_parent(self):
        text = "\nclass name : public parent\n {\n nnext{line}\n }\n"
        iStart = text.find('{')
        iEnd = text.find('}', iStart+1)
        b = Block(None, text, iStart, iEnd)
        self.assertEqual('class name : public parent', b.m_strHeader)
        self.assertEqual(BlockType.CLASSSTRUCT, b.m_Type)

    def test_block_class_twoline_parent(self):
        text = "\nclass name :\n public parent\n {\n nnext{line}\n }\n"
        iStart = text.find('{')
        iEnd = text.find('}', iStart+1)
        b = Block(None, text, iStart, iEnd)
        self.assertEqual('class name', b.m_strHeader)
        self.assertEqual(BlockType.CLASSSTRUCT, b.m_Type)

    # test functions
    def test_block_func(self):
        text = "\ntype name(params)\n {\n nnext{line}\n }\n"
        iStart = text.find('{')
        iEnd = text.find('}', iStart+1)
        b = Block(None, text, iStart, iEnd)
        self.assertEqual('type name', b.m_strHeader)
        self.assertEqual(BlockType.FUNCTION, b.m_Type)
        self.assertEqual("name", b.m_strFunctionName)
        self.assertEqual("", b.m_strNamespace)

    def test_block_func_oldstyle(self):
        text = "\ntype\nname(params)\n {\n nnext{line}\n }\n"
        iStart = text.find('{')
        iEnd = text.find('}', iStart+1)
        b = Block(None, text, iStart, iEnd)
        self.assertEqual('name', b.m_strHeader)
        self.assertEqual(BlockType.FUNCTION, b.m_Type)
        self.assertEqual("name", b.m_strFunctionName)
        self.assertEqual("", b.m_strNamespace)

    def test_block_func_std(self):
        text = "\nstd::string name(params)\n {\n nnext{line}\n }\n"
        iStart = text.find('{')
        iEnd = text.find('}', iStart+1)
        b = Block(None, text, iStart, iEnd)
        self.assertEqual('std::string name', b.m_strHeader)
        self.assertEqual(BlockType.FUNCTION, b.m_Type)
        self.assertEqual("name", b.m_strFunctionName)
        self.assertEqual("", b.m_strNamespace)

    def test_block_func_ptr(self):
        text = "\ntype **name(params)\n {\n nnext{line}\n }\n"
        iStart = text.find('{')
        iEnd = text.find('}', iStart+1)
        b = Block(None, text, iStart, iEnd)
        self.assertEqual('type **name', b.m_strHeader)
        self.assertEqual(BlockType.FUNCTION, b.m_Type)
        self.assertEqual("name", b.m_strFunctionName)
        self.assertEqual("", b.m_strNamespace)

    def test_block_func_ref(self):
        text = "\ntype &name(params)\n {\n nnext{line}\n }\n"
        iStart = text.find('{')
        iEnd = text.find('}', iStart+1)
        b = Block(None, text, iStart, iEnd)
        self.assertEqual('type &name', b.m_strHeader)
        self.assertEqual(BlockType.FUNCTION, b.m_Type)
        self.assertEqual("name", b.m_strFunctionName)
        self.assertEqual("", b.m_strNamespace)

    def test_block_func_mixed_ptr_ref(self):
        text = "\ntype &*name(params)\n {\n nnext{line}\n }\n"
        iStart = text.find('{')
        iEnd = text.find('}', iStart+1)
        b = Block(None, text, iStart, iEnd)
        self.assertEqual('type &*name', b.m_strHeader)
        self.assertEqual(BlockType.FUNCTION, b.m_Type)
        self.assertEqual("name", b.m_strFunctionName)
        self.assertEqual("", b.m_strNamespace)

    def test_block_class_func_ptr(self):
        text = "\ntype **class::name(params)\n {\n nnext{line}\n }\n"
        iStart = text.find('{')
        iEnd = text.find('}', iStart+1)
        b = Block(None, text, iStart, iEnd)
        self.assertEqual('type **class::name', b.m_strHeader)
        self.assertEqual(BlockType.FUNCTION, b.m_Type)
        self.assertEqual("name", b.m_strFunctionName)
        self.assertEqual("class", b.m_strNamespace)

    def test_block_class_func_ref(self):
        text = "\ntype &class::name(params)\n {\n nnext{line}\n }\n"
        iStart = text.find('{')
        iEnd = text.find('}', iStart+1)
        b = Block(None, text, iStart, iEnd)
        self.assertEqual('type &class::name', b.m_strHeader)
        self.assertEqual(BlockType.FUNCTION, b.m_Type)
        self.assertEqual("name", b.m_strFunctionName)
        self.assertEqual("class", b.m_strNamespace)

    def test_block_class_func_ptr_twoline_param(self):
        text = "\ntype **class::name(param1,\nparam2)\n {\n nnext{line}\n }\n"
        iStart = text.find('{')
        iEnd = text.find('}', iStart+1)
        b = Block(None, text, iStart, iEnd)
        self.assertEqual('type **class::name', b.m_strHeader)
        self.assertEqual(BlockType.FUNCTION, b.m_Type)
        self.assertEqual("name", b.m_strFunctionName)
        self.assertEqual("class", b.m_strNamespace)

    def test_block_class_func_twoline(self):
        text = "\ntype **class::\nname(param1,param2)\n {\n nnext{line}\n }\n"
        iStart = text.find('{')
        iEnd = text.find('}', iStart+1)
        b = Block(None, text, iStart, iEnd)
        self.assertEqual('type **class::name', b.m_strHeader)
        self.assertEqual(BlockType.FUNCTION, b.m_Type)
        self.assertEqual("name", b.m_strFunctionName)
        self.assertEqual("class", b.m_strNamespace)

    def test_block_class_func_std(self):
        text = "\nstd::string class::name(params)\n {\n nnext{line}\n }\n"
        iStart = text.find('{')
        iEnd = text.find('}', iStart+1)
        b = Block(None, text, iStart, iEnd)
        self.assertEqual('std::string class::name', b.m_strHeader)
        self.assertEqual(BlockType.FUNCTION, b.m_Type)
        self.assertEqual("name", b.m_strFunctionName)
        self.assertEqual("class", b.m_strNamespace)

    def test_block_class_func_multiple(self):
        text = "\nstd::string class::inner::name(params)\n {\n nnext{line}\n }\n"
        iStart = text.find('{')
        iEnd = text.find('}', iStart+1)
        b = Block(None, text, iStart, iEnd)
        self.assertEqual('std::string class::inner::name', b.m_strHeader)
        self.assertEqual(BlockType.FUNCTION, b.m_Type)
        self.assertEqual("name", b.m_strFunctionName)
        self.assertEqual("class::inner", b.m_strNamespace)

    def test_block_class_func_const(self):
        text = "\nstd::string class::name(params) const\n {\n nnext{line}\n }\n"
        iStart = text.find('{')
        iEnd = text.find('}', iStart+1)
        b = Block(None, text, iStart, iEnd)
        self.assertEqual('std::string class::name', b.m_strHeader)
        self.assertEqual(BlockType.FUNCTION, b.m_Type)
        self.assertEqual("name", b.m_strFunctionName)
        self.assertEqual("class", b.m_strNamespace)

    def test_block_class_func_const_throw(self):
        text = "\nconst std::string& class::name(params) const throw(exception)\n {\n nnext{line}\n }\n"
        iStart = text.find('{')
        iEnd = text.find('}', iStart+1)
        b = Block(None, text, iStart, iEnd)
        self.assertEqual('const std::string& class::name', b.m_strHeader)
        self.assertEqual(BlockType.FUNCTION, b.m_Type)
        self.assertEqual("name", b.m_strFunctionName)
        self.assertEqual("class", b.m_strNamespace)

    # test classes
    def test_block_class_constr(self):
        text = "\nclass::name(param1,param2)\n {\n nnext{line}\n }\n"
        iStart = text.find('{')
        iEnd = text.find('}', iStart+1)
        b = Block(None, text, iStart, iEnd)
        self.assertEqual('class::name', b.m_strHeader)
        self.assertEqual(BlockType.FUNCTION, b.m_Type)
        self.assertEqual("name", b.m_strFunctionName)
        self.assertEqual("class", b.m_strNamespace)

    def test_block_class_constr_parent_oneline(self):
        text = "\nclass::name(param1,param2) : parent(param1), member(param2)\n {\n nnext{line}\n }\n"
        iStart = text.find('{')
        iEnd = text.find('}', iStart+1)
        b = Block(None, text, iStart, iEnd)
        self.assertEqual('class::name', b.m_strHeader)
        self.assertEqual(BlockType.FUNCTION, b.m_Type)
        self.assertEqual("name", b.m_strFunctionName)
        self.assertEqual("class", b.m_strNamespace)

    def test_block_class_constr_parent_twoline(self):
        text = "\nclass::name(param1,param2) :\n parent(param1), member(param2)\n {\n nnext{line}\n }\n"
        iStart = text.find('{')
        iEnd = text.find('}', iStart+1)
        b = Block(None, text, iStart, iEnd)
        self.assertEqual('class::name', b.m_strHeader)
        self.assertEqual(BlockType.FUNCTION, b.m_Type)
        self.assertEqual("name", b.m_strFunctionName)
        self.assertEqual("class", b.m_strNamespace)

    def test_block_class_constr_parent_twoline2(self):
        text = "\nclass::name(param1,param2)\n: parent(param1), member(param2)\n {\n nnext{line}\n }\n"
        iStart = text.find('{')
        iEnd = text.find('}', iStart+1)
        b = Block(None, text, iStart, iEnd)
        self.assertEqual('class::name', b.m_strHeader)
        self.assertEqual(BlockType.FUNCTION, b.m_Type)
        self.assertEqual("name", b.m_strFunctionName)
        self.assertEqual("class", b.m_strNamespace)

    def test_block_class_constr_parent_allline(self):
        text = "\nclass::name(param1,param2)\n: parent(param1)\n, member(param2)\n {\n nnext{line}\n }\n"
        iStart = text.find('{')
        iEnd = text.find('}', iStart+1)
        b = Block(None, text, iStart, iEnd)
        self.assertEqual('class::name', b.m_strHeader)
        self.assertEqual(BlockType.FUNCTION, b.m_Type)
        self.assertEqual("name", b.m_strFunctionName)
        self.assertEqual("class", b.m_strNamespace)

    def test_block_class_constr_parent_allline_with_empty(self):
        text = "\nclass::name(param1,param2)\n\n: parent(param1)\n\n, member(param2)\n\n {\n nnext{line}\n }\n"
        iStart = text.find('{')
        iEnd = text.find('}', iStart+1)
        b = Block(None, text, iStart, iEnd)
        self.assertEqual('class::name', b.m_strHeader)
        self.assertEqual(BlockType.FUNCTION, b.m_Type)
        self.assertEqual("name", b.m_strFunctionName)
        self.assertEqual("class", b.m_strNamespace)

    def test_block_class_constr_parent_allline_with_note(self):
        text = "\nclass::name(param1,param2)\n// note\n: parent(param1)\n//note\n, member(param2)\n\n {\n nnext{line}\n }\n"
        iStart = text.find('{')
        iEnd = text.find('}', iStart+1)
        b = Block(None, text, iStart, iEnd)
        self.assertEqual('class::name', b.m_strHeader)
        self.assertEqual(BlockType.FUNCTION, b.m_Type)
        self.assertEqual("name", b.m_strFunctionName)
        self.assertEqual("class", b.m_strNamespace)

    def test_ToString(self):
        text = "\ntype class::name(params)\n {\n nnext{line}\n }\n"
        iStart = text.find('{')
        iEnd = text.find('}', iStart+1)
        b = Block(None, text, iStart, iEnd)
        self.assertEqual('type class::name', b.m_strHeader)
        self.assertEqual(BlockType.FUNCTION, b.m_Type)
        self.assertEqual("name", b.m_strFunctionName)
        self.assertEqual("class", b.m_strNamespace)
        self.assertEqual("class::name", str(b))

    def test_GetNamespace(self):
        text = "\n\nclass::name(param1,param2) \n {\n nnext{line}\n }\n"
        iStart = text.find('{')
        iEnd = text.find('}', iStart + 1)
        b = Block(None, text, iStart, iEnd)
        self.assertEqual('class::name', b.m_strHeader)
        self.assertEqual(BlockType.FUNCTION, b.m_Type)
        self.assertEqual("name", b.m_strFunctionName)
        self.assertEqual("class", b.m_strNamespace)
        self.assertEqual("class", b.GetNamespace())

    def test_GetNamespace_parent(self):
        text = "\nnamespace nsp {\nclass::name(param1,param2) \n {\n nnextline}\n }\n"
        iStart1 = text.find('{')
        iStart2 = text.rfind('{')
        iEnd1 = text.rfind('}')
        iEnd2 = text.find('}')
        parent = Block(None, text, iStart1, iEnd1)
        nested = Block(parent, text, iStart2, iEnd2)
        self.assertEqual(BlockType.NAMESPACE, parent.m_Type)
        self.assertEqual(BlockType.FUNCTION, nested.m_Type)
        self.assertEqual("nsp::class", nested.GetNamespace())
