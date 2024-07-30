from unittest import TestCase
from app.optionbase import OptionBase


class TestOptionBase(TestCase):
    def test_const(self):
        o = OptionBase()
        self.assertFalse(o.isDebug)
        self.assertFalse(o.isVerbose)
        self.assertFalse(o.isLog)
