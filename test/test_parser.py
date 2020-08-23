import unittest
from parser import XLSXParser
import settings
import io


class TestParser(unittest.TestCase):

    def test_find_data_sheet(self):
        file_path = f'{settings.BASE_DIR}/data/example.xlsx'
        parser = XLSXParser(file_path)
        sheet = parser._find_data_sheet()
        pass

    def test_parse(self):
        file_path = f'{settings.BASE_DIR}/data/example.xlsx'
        parser = XLSXParser(file_path)
        sheet = parser.parse()
        pass
