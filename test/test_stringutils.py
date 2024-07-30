from unittest import TestCase
from parser.stringutils import StringUtils


class TestStringUtils(TestCase):

    def test_FindPrev(self):
        str = "Ez egy string, amiben van vesszo."
        idx1 = str.find(',')
        self.assertEqual(-1, StringUtils.FindPrev(str, idx1, ','))

    def test_FindPrev2(self):
        str = "Ez egy string, amiben van vesszo, ketszer is."
        idx1 = str.find(',')
        idx2 = str.find(',', idx1 + 1)
        self.assertEqual(idx1, StringUtils.FindPrev(str, idx2, ','))

    def test_FindPrevX(self):
        str = "Ez egy string zarojel nelkul)."
        idx1 = str.find('(')
        idx2 = str.rfind(')')
        self.assertEqual(idx1, StringUtils.FindPrevX(str, idx2, '(', ')'))

    def test_FindPrevX2(self):
        str = "Ez egy string( amiben van zarojel)."
        idx1 = str.find('(')
        idx2 = str.rfind(')')
        self.assertEqual(idx1, StringUtils.FindPrevX(str, idx2, '(', ')'))

    def test_FindPrevX3(self):
        str = "Ez egy string( amiben (van) zarojel)."
        idx1 = str.find('(')
        idx2 = str.rfind(')')
        self.assertEqual(idx1, StringUtils.FindPrevX(str, idx2, '(', ')'))

    def test_GetCount(self):
        str = "almafa"
        self.assertEqual(3, StringUtils.GetCount(str, 'a'))

    def test_GetCount2(self):
        str = "almafa"
        self.assertEqual(0, StringUtils.GetCount(str, 'x'))

    def test_GetCount3(self):
        str = ""
        self.assertEqual(0, StringUtils.GetCount(str, 'x'))

    def test_GetCount4(self):
        str = "almafa"
        self.assertEqual(0, StringUtils.GetCount(str, ''))

    def test_RemoveComment(self):
        str = "almafa // comment"
        self.assertEqual("almafa ", StringUtils.RemoveComment(str))

    def test_RemoveComment2(self):
        str = "almafa /* comment */ folytat"
        self.assertEqual("almafa  folytat", StringUtils.RemoveComment(str))

    def test_RemoveComment3(self):
        str = "almafa /* comment */ folytat /* ujabb comment */ eddig"
        self.assertEqual("almafa  folytat  eddig", StringUtils.RemoveComment(str))

    def test_RemoveComment4(self):
        str = "almafa /* comment */ folytat // vegyes commenttel"
        self.assertEqual("almafa  folytat ", StringUtils.RemoveComment(str))

    def test_GetPrevLine(self):
        str = "Ez egy string es negativ start index"
        self.assertEqual("", StringUtils.GetPrevLine(str, -1))

    def test_GetPrevLine2(self):
        str = "Ez egy egysoros string"
        self.assertEqual("", StringUtils.GetPrevLine(str, len(str)))

    def test_GetPrevLine3(self):
        str = "Ez egy harom \n soros string, \n es innen keresunk"
        self.assertEqual("soros string,", StringUtils.GetPrevLine(str, str.rfind('\n')))

    def test_GetPrevLine4(self):
        str = "Ez egy negy \n soros string, \n# ahol ez kimarad \n es innen keresunk"
        self.assertEqual("soros string,", StringUtils.GetPrevLine(str, str.rfind('\n')))

    def test_GetPrevLine5(self):
        str = "Ez egy negy \n soros string, \n// ahol ez kimarad \n es innen keresunk"
        self.assertEqual("soros string,", StringUtils.GetPrevLine(str, str.rfind('\n')))

    def test_GetPrevLine6(self):
        str = "Ez egy sok \n soros string, \n\n\n\n ahol az ures sorok kimaradnak es innen keresunk"
        self.assertEqual("soros string,", StringUtils.GetPrevLine(str, str.rfind('\n')))
