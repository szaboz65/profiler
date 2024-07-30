'''
Coding class
'''

import codecs


class Coding(object):
    '''
    // Function to detect the encoding for UTF-7, UTF-8/16/32 (bom, no bom, little
    // & big endian), and local default codepage, and potentially other codepages.
    // 'taster' = number of bytes to check of the file (to save processing). Higher
    // value is slower, but more reliable (especially UTF-8 with special characters
    // later on may appear to be ASCII initially). If taster = 0, then taster
    // becomes the length of the file (for maximum reliability). 'text' is simply
    // the string with the discovered encoding applied to the file.
    '''

    def __init__(self, filename, taster=1000):
        self._filename = filename
        self._skip = 0
        self._encoding = None
        self._taster = taster
        if filename != "":
            self.detectTextEncoding()

    def detectTextEncoding(self):
        with open(self._filename, 'rb') as f:
            b = f.read(self._taster)

            # //////////////// First check the low-hanging fruit by checking if a
            # //////////////// BOM/signature exists (sourced from http://www.unicode.org/faq/utf_bom.html#bom4)
            encoders = [
                {'bom': codecs.BOM_UTF32, 'encoding': 'utf-32', 'skip': 1},
                {'bom': codecs.BOM_UTF32_LE, 'encoding': 'utf-32_le', 'skip': 0},
                {'bom': codecs.BOM_UTF32_BE, 'encoding': 'utf-32_be', 'skip': 0},
                {'bom': codecs.BOM_UTF16, 'encoding': 'utf-16', 'skip': 0},
                {'bom': codecs.BOM_UTF16_LE, 'encoding': 'utf-16_le', 'skip': 0},
                {'bom': codecs.BOM_UTF16_BE, 'encoding': 'utf-16_be', 'skip': 1},
                {'bom': codecs.BOM_UTF8, 'encoding': 'utf-8', 'skip': 1}
            ]

            def detect_bom():
                for item in encoders:
                    if len(b) >= len(item['bom']) and b[:len(item['bom'])] == item['bom']:
                        return item
                return None

            # check the boom
            encoder = detect_bom()
            if encoder is not None:
                self._skip = encoder['skip']
                self._encoding = encoder['encoding']
                return True

            # //////////// If the code reaches here, no BOM/signature was found, so now
            # //////////// we need to 'taste' the file to see if it can manually discover
            # //////////// the encoding. A high taster value is desired for UTF-8
            if self._taster == 0 or self._taster > len(b):
                self._taster = len(b)  # // Taster size can't be bigger than the filesize, obviously.

            # // Some text files are encoded in UTF8, but have no BOM/signature.
            # // Hence the below manually checks for a UTF8 pattern. This code is based off
            # // the top answer at: http://stackoverflow.com/questions/6555015/check-for-invalid-utf8
            # // For our purposes, an unnecessarily strict (and terser/slower)
            # // implementation is shown at: http://stackoverflow.com/questions/1031645/how-to-detect-utf-8-in-plain-c
            # // For the below, false positives should be exceedingly rare (and would
            # // be either slightly malformed UTF-8 (which would suit our purposes
            # // anyway) or 8-bit extended ASCII/UTF-16/32 at a vanishingly long shot).
            def detect_utf8():
                i = 0
                isutf8 = False

                def isnext(x):
                    return x >= 0x80 and x < 0xC0

                # // If all characters are below 0x80, then it is valid UTF8, but UTF8 is not 'required'
                # (and therefore the text is more desirable to be treated as the default codepage of the computer).
                # Hence, there's no "utf8 = true;" code unlike the next three checks.
                while i < self._taster - 4:
                    # range: U-00000000 ... U-0000007F	encoding: 0xxxxxxx
                    if b[i] <= 0x7F:
                        i += 1
                        continue

                    # range: U-00000080 ... U-000007FF	encoding: 110xxxxx 10xxxxxx
                    if b[i] >= 0xC0 and b[i] < 0xE0 and isnext(b[i + 1]):
                        i += 2
                        isutf8 = True
                        continue

                    # range: U-00000800 ... U-0000FFFF	encoding: 1110xxxx 10xxxxxx 10xxxxxx
                    if b[i] >= 0xE0 and b[i] < 0xF0 and isnext(b[i + 1]) and isnext(b[i + 2]):
                        i += 3
                        isutf8 = True
                        continue

                    # range: U-00010000 ... U-0010FFFF	11110xxx 10xxxxxx 10xxxxxx 10xxxxxx
                    if b[i] >= 0xF0 and b[i] < 0xF8 and isnext(b[i + 1]) and isnext(b[i + 2]) and isnext(b[i + 3]):
                        i += 4
                        isutf8 = True
                        continue

                    isutf8 = False
                    break
                return isutf8

            utf8 = detect_utf8()
            if utf8 is True:
                self._encoding = 'utf-8'
                return True

            # The next check is a heuristic attempt to detect UTF-16 without a BOM.
            # We simply look for zeroes in odd or even byte places, and if a certain
            # threshold is reached, the code is 'probably' UF-16.
            def detect_utf16(bigendian):
                threshold = 0.1  # proportion of chars step 2 which must be zeroed to be diagnosed as utf-16. 0.1 = 10%
                count = 0
                n = 0 if bigendian else 1
                while n < self._taster:
                    if b[n] == 0:
                        count += 1
                    n += 2
                return count > self._taster * threshold

            # check(big-endian)
            if detect_utf16(True):
                self._encoding = 'utf-16_be'
                return True

            # check(little-endian)
            if detect_utf16(False):
                self._encoding = 'utf-16_le'
                return True

            # // Finally, a long shot - let's see if we can find "charset=xyz" or
            # // "encoding=xyz" to identify the encoding:
            def match(x):
                size = len(x)
                for i in range(self._taster-size):
                    matched = True
                    for j in range(size):
                        if b[i+j] != ord(x[j]):
                            matched = False
                            break
                    if matched:
                        return i + size
                return -1

            def isvalid_encoder(x):
                for i in range(len(encoders)):
                    if encoders[i]['encoding'] == x:
                        return True
                return False

            pos = match("charset=")
            if pos == -1:
                pos = match("encoding=")
            if pos != -1:
                delimiter = chr(b[pos])
                # get the value: "utf-xxx"
                if delimiter == '"' or delimiter == '\'':
                    pos += 1
                    encoding = ''
                    while pos < self._taster and chr(b[pos]) != delimiter:
                        ch = chr(b[pos])
                        if ch in '_-' or ch.isdigit() or ch.islower() or ch.isupper():
                            encoding += ch
                            pos += 1

                    # set if valid
                    if isvalid_encoder(encoding):
                        self._encoding = encoding
                        return True

            # If all else fails, the encoding is probably (though certainly not
            # definitely) the user's local codepage! One might present to the user a
            # list of alternative encodings as shown here:
            # http://stackoverflow.com/questions/8509339/what-is-the-most-common-encoding-of-each-language
            # A full list can be found using Encoding.GetEncodings();
            # text = Encoding.Default.GetString(b);
            self._encoding = None
            return True

    def _get_encoding(self):
        return self._encoding

    encoding = property(_get_encoding)

    def readFile(self):
        with codecs.open(self._filename, mode='r', encoding=self._encoding) as f:
            t = f.read()
            if self._skip > 0:
                return t[self._skip:]
            return t

    def writeFile(self, text):
        with codecs.open(self._filename, mode="w", encoding=self.encoding) as f:
            f.write(text)
            return True
