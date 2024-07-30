from unittest import TestCase
from statfile.csvfile import NumCsvFile, CsvFile


class TestCsvFile(TestCase):
    def test_constr(self):
        csv = CsvFile()
        self.assertEqual(0, len(csv.header))
        self.assertEqual(0, len(csv.data))

    def test_Clear(self):
        csv = CsvFile()
        csv.SetHeader('id', 'count')
        csv.AddData(11, 12)
        csv.Clear()
        self.assertEqual(0, len(csv.header))
        self.assertEqual(0, len(csv.data))

    def test_SetHeader(self):
        csv = CsvFile()
        csv.SetHeader('id', 'count')
        self.assertEqual(2, len(csv.header))

    def test_AddData_num(self):
        csv = NumCsvFile()
        csv.SetHeader('id', 'count')
        csv.AddData(11, 12)
        csv.AddData(21, 22)
        self.assertEqual(2, len(csv.data))
        self.assertEqual(11, csv.data[0][0])
        self.assertEqual(12, csv.data[0][1])
        self.assertEqual(21, csv.data[1][0])
        self.assertEqual(22, csv.data[1][1])

    def test_AddData_str(self):
        csv = CsvFile()
        csv.SetHeader('id', 'count')
        csv.AddData('11', '12')
        csv.AddData('21', '22')
        self.assertEqual(2, len(csv.data))
        self.assertEqual('11', csv.data[0][0])
        self.assertEqual('12', csv.data[0][1])
        self.assertEqual('21', csv.data[1][0])
        self.assertEqual('22', csv.data[1][1])

    def test_ToString(self):
        csv = CsvFile()
        csv.SetHeader('id', 'count')
        csv.AddData('11', '12')
        csv.AddData('21', '22')
        strText = csv.ToString()
        self.assertEqual("id;count\n11;12\n21;22\n", strText)

    def test_parseString(self):
        strText = "id;count\n11;12\n21;22\n"
        csv = CsvFile()
        csv.parseString(strText)
        self.assertEqual(2, len(csv.header))
        self.assertEqual(2, len(csv.data))
        self.assertEqual('11', csv.data[0][0])
        self.assertEqual('12', csv.data[0][1])
        self.assertEqual('21', csv.data[1][0])
        self.assertEqual('22', csv.data[1][1])

    def test_SaveFile(self):
        strText = "id;count\n11;12\n21;22\n"
        csv = CsvFile()
        csv.parseString(strText)
        csv.SaveFile("test/csv.csv")

        with open("test/csv.csv") as f:
            text = f.read()
            self.assertEqual(strText, text)
            lines = text.splitlines()
            self.assertEqual(3, len(lines))

    def test_LoadFile(self):
        csv = CsvFile()
        csv.LoadFile("test/csv.csv")
        self.assertEqual(2, len(csv.header))
        self.assertEqual(2, len(csv.data))
        self.assertEqual('11', csv.data[0][0])
        self.assertEqual('12', csv.data[0][1])
        self.assertEqual('21', csv.data[1][0])
        self.assertEqual('22', csv.data[1][1])


class TestNumCsv(TestCase):

    def test_ToString_num(self):
        csv = NumCsvFile()
        csv.SetHeader('id', 'count')
        csv.AddData(11, 12)
        csv.AddData(21, 22)
        strText = csv.ToString()
        self.assertEqual("id;count\n11;12\n21;22\n", strText)

    def test_parseString_num(self):
        strText = "id;count\n11;12\n21;22\n"
        csv = NumCsvFile()
        csv.parseString(strText)
        self.assertEqual(2, len(csv.header))
        self.assertEqual(2, len(csv.data))
        self.assertEqual(11, csv.data[0][0])
        self.assertEqual(12, csv.data[0][1])
        self.assertEqual(21, csv.data[1][0])
        self.assertEqual(22, csv.data[1][1])
