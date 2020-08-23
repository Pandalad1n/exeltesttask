import openpyxl


class XLSXParser:
    def __init__(self, file_path):
        self.book = openpyxl.load_workbook(file_path)

    def _find_data_sheet(self):
        after_index, before_index = None, None
        for sheet in self.book:
            first_row = next(sheet.rows, None)
            if not first_row:
                continue
            for i, cell in enumerate(first_row):
                if cell.value == '':
                    break
                if cell.value == 'after':
                    after_index = i
                if cell.value == 'before':
                    before_index = i
                if (after_index is not None) and (before_index is not None):
                    return sheet, after_index, before_index
        return None, None, None

    def parse(self):
        sheet, after_index, before_index = self._find_data_sheet()
        if sheet is None:
            return None
        after_sum, before_sum = 0, 0
        rows = iter(sheet.rows)
        next(rows)
        for row in rows:
            after_sum += int(row[after_index].value or 0)
            before_sum += int(row[before_index].value or 0)
        return before_sum - after_sum
