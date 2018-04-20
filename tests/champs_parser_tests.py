import unittest
from parsers.champsparser import *
PATH = '../data/2018'


class ChampsParserTests(unittest.TestCase):

    def setUp(self):
        self.records = ResultParser(f'{PATH}/raw/champs18.txt').get_records()

    def test_champs18_parsing(self):
        self.assertEqual(4313, len(self.records.index))

    def test_parsed_disqualifications(self):
        dq = self.records[self.records.Mark=='DQ']
        self.assertEqual(57, len(dq.index))

    def test_parse_dnfs(self):
        dnfs = self.records[self.records.Mark == 'DNF']
        self.assertEqual(37, len(dnfs.index))


if __name__ == '__main__':
    unittest.main()