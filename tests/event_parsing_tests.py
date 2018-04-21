import unittest
from parsers.champsparser import *


eventParser = LineParser('Event [0-9]{1,3} *(Decathlon: #1 *)?GENDER [0-9]{1,2}\-[0-9]{1,2} EVENT *CLASS',
                         lambda match: {'Gender': match.group(2), 'Event':match.group(3), 'Class': match.group(6)})

def match(regex, line):
    m = re.match(regex,line)
    m_groups = (m.group(0), m.groups()) if m else None
    return m_groups

class EventParsingTest(unittest.TestCase):

    def test_parse_decathlon_event(self):
        event = eventParser.get_record('Event 40  Decathlon: #1 Boys 14-19 100 Meter Run Decathlon')
        self.assertIsNotNone(event)
        self.assertEquals(('Boys', '100 Meter Run', 'Decathlon'), ( event['Gender'], event['Event'], event['Class']))



if __name__ == '__main__':
    unittest.main()