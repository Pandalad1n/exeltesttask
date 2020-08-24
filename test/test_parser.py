import unittest
from parser import XLSXParser
import settings
import io


class TestParser(unittest.TestCase):

    def test_find_data_sheet(self):
        file_path = f'{settings.BASE_DIR}/data/example.xlsx'
        parser = XLSXParser(file_path)
        sheet = parser._find_data_sheet()
        self.assertEquals(sheet.count(3), 1)
        self.assertEquals(sheet.count(2), 1)

    def test_parse(self):
        file_path = f'{settings.BASE_DIR}/data/example.xlsx'
        parser = XLSXParser(file_path)
        parsed = parser.parse()
        self.assertEquals(parsed, -5)
