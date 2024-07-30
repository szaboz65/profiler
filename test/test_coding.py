from unittest import TestCase
from parser.coding import Coding


class TestCoding(TestCase):
    text_pi = u'pi: \u03c0'
    text_pia = u'pi: a'

    def test__const(self):
        c = Coding("")
        self.assertEqual(0, c._skip, "Default skip")
        self.assertEqual(None, c._encoding, "Default encoding")
        self.assertEqual("", c._filename, "Default filename")
        self.assertEqual(1000, c._taster, "Default taster")

    def test__get_encoding(self):
        c = Coding("")
        self.assertEqual(None, c.encoding, "Default encoding")

    # test for bom
    def test_detectTextEncoding_utf8_bom(self):
        c = Coding("test\\utf_8_bom.txt")
        self.assertEqual('utf-8', c.encoding)
        text = c.readFile()
        text = text[0: text.find("\r")]
        self.assertEqual(self.text_pi, text)

    def test_detectTextEncoding_utf16_bom(self):
        c = Coding("test\\utf-16.txt")
        self.assertEqual('utf-16', c.encoding)
        text = c.readFile()
        text = text[0: text.find("\r")]
        self.assertEqual(self.text_pi, text)

    def test_detectTextEncoding_utf16_le_bom(self):
        c = Coding("test\\utf_16_le_bom.txt")
        self.assertEqual('utf-16', c.encoding)
        text = c.readFile()
        text = text[0: text.find("\r")]
        self.assertEqual(self.text_pi, text)

    def test_detectTextEncoding_utf16_be_bom(self):
        c = Coding("test\\utf_16_be_bom.txt")
        self.assertEqual('utf-16_be', c.encoding)
        text = c.readFile()
        text = text[0: text.find("\r")]
        self.assertEqual(self.text_pi, text)

    # tests without bom
    def test_detectTextEncoding_utf8_wobom(self):
        c = Coding("test\\utf-8.txt")
        self.assertEqual('utf-8', c.encoding)
        text = c.readFile()
        text = text[0: text.find("\r")]
        self.assertEqual(self.text_pi, text)

    def test_detectTextEncoding_utf16_le_wobom(self):
        c = Coding("test\\utf-16_le.txt")
        self.assertEqual('utf-16_le', c.encoding)
        text = c.readFile()
        text = text[0: text.find("\r")]
        self.assertEqual(self.text_pi, text)

    def test_detectTextEncoding_utf16_be_wobom(self):
        c = Coding("test\\utf-16_be.txt")
        self.assertEqual('utf-16_be', c.encoding)
        text = c.readFile()
        self.assertEqual(self.text_pi, text)

    '''
    # UTF32 Not implemented
    def test_detectTextEncoding_utf32_bom(self):
        c = Coding("test\\utf-32_bom.txt")
        self.assertEqual('utf-32', c.encoding)
        text = c.readFile()
        text = text[0: text.find(u"\r")]
        self.assertEqual(self.text_pi, text)

    def test_detectTextEncoding_utf32_le_wobom(self):
        c = Coding("test\\utf-32_le.txt")
        self.assertEqual('utf-32_le', c.encoding)
        text = c.readFile()
        text = text[0: text.find("\r")]
        self.assertEqual(self.text_pi, text)

    def test_detectTextEncoding_utf32_be_wobom(self):
        c = Coding("test\\utf-32_be.txt")
        self.assertEqual('utf-32_be', c.encoding)
        text = c.readFile()
        text = text[0: text.find("\r")]
        self.assertEqual(self.text_pi, text)
    '''

    # test for ansi
    def test_detectTextEncoding_charset(self):
        c = Coding("test\\charset.txt")
        self.assertEqual('utf-8', c.encoding)
        text = c.readFile()
        text = text[0: text.find("\r")]
        self.assertEqual(self.text_pia, text)

    def test_detectTextEncoding_encoding(self):
        c = Coding("test\\encoding.txt")
        self.assertEqual('utf-8', c.encoding)
        text = c.readFile()
        text = text[0: text.find("\r")]
        self.assertEqual(self.text_pia, text)

    def test_detectTextEncoding_ansi(self):
        c = Coding("test\\ansi.txt")
        self.assertEqual(None, c.encoding)
        text = c.readFile()
        text = text[0: text.find("\n")]
        self.assertEqual(self.text_pia, text)
