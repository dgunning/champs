from parsers.champsparser import *
import re
import unittest


def match(regex, line):
    m = re.match(regex,line)
    m_groups = (m.group(0), m.groups()) if m else None
    return m_groups


class PointsTest(unittest.TestCase):

    def test_does_not_match_zero(self):
        self.assertIsNone(match(POINTS, '0'))

    def test_does_not_match_negative(self):
        self.assertIsNone(match(POINTS, '-1'))

    def test_expected_integer_points(self):
        self.assertEqual('1', match(POINTS, '1')[0])
        self.assertEqual('2', match(POINTS, '2')[0])
        self.assertEqual('9', match(POINTS, '9')[0])
        self.assertEqual('10', match(POINTS, '10')[0])
        self.assertEqual('12', match(POINTS, '12')[0])

    def test_does_not_match_eleven(self):
        self.assertIsNone(match(POINTS, '11'))

    def test_match_partial_points(self):
        self.assertEqual('5.50', match(POINTS, '5.50')[0])
        self.assertEqual('0.20', match(POINTS, '0.20')[0])
        self.assertIsNone(match(POINTS, '5.5'))

    def test_parse_disqualified(self):
        self.assertEquals('DQ  RULE 163.6', match(DISQUALIFICATION, 'DQ  RULE 163.6')[0])
        self.assertEquals('DQ  RULE 170.15', match(DISQUALIFICATION, 'DQ  RULE 170.15')[0])
        self.assertEquals('DQ  RULE 163.3B', match(DISQUALIFICATION, 'DQ  RULE 163.3B')[0])
        self.assertEquals('DQ  RULE 170.15', match(DISQUALIFICATION, 'DQ  RULE 170.15')[0])
        self.assertEquals('DQ  IAAF RULE 163.3B', match(DISQUALIFICATION, 'DQ  IAAF RULE 163.3B')[0])
        self.assertEquals('DQ   ISSA RULE 5b', match(DISQUALIFICATION, 'DQ   ISSA RULE 5b')[0])

    def test_rank(self):
        self.assertEquals('--', match(RANK, '--')[0])
        self.assertEquals(' --', match(RANK, ' --')[0])
        self.assertEquals('---', match(RANK, '---')[0])
        self.assertEquals('5', match(RANK, '5')[0])
        self.assertEquals('14', match(RANK, '14')[0])


if __name__ == '__main__':
    unittest.main()