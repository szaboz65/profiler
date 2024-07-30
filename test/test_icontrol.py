from unittest import TestCase
from appppm.icontrol import IControl


class TestIControl(TestCase):
    def test_const(self):
        c = IControl()
        self.assertEqual("", c.LastParsedFile)
