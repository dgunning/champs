import re
import pandas as pd


def regex_choices(options, brackets=True):
    opts ='|'.join(options)
    return f'({opts})' if brackets else opts


def get_lines(data_file):
    SKIPS = ['==','Sponsor']
    with open(data_file, 'r') as f:
        for line in f:
            stripped_line = line.strip()
            if stripped_line:
                if not any([skip in stripped_line for skip in SKIPS]):
                    yield stripped_line


def trim(string, value_if_none=None):
    return string.strip() if string else value_if_none


EVENT= regex_choices( [
    '[0-9]{,5} Meter (Dash|Run|Hurdles|Steeplechase)',
    '4x[1-9]+00 Meter Relay',
    'Javelin Throw',
    'Discus Throw',
    'Shot Put',
    'Pole Vault',
    '(Long|High|Triple) Jump',
    '1 Mile Run',
    '1600 Sprint Medley',
    'Decathlon',
    'Heptathlon'
])

print(EVENT)
CLASS = '(CLASS [1-4]|Open|Decathlon|Heptathlon)'
DISQUALIFICATION = 'DQ( {1,4}(((IAAF|ISSA) )?RULE)? [0-9]{1,4}(\.[0-9]{1,2})?[A-Za-z]?)'
RANK = ' *([0-9]{1,3}|\-{1,4})'
COMP_NUM = '# {1,4}([0-9]{1,4})'
WORD = '[\w\'\.\-]+'
ROUND = '((Flight|Heat|Section) *[0-9]+)? *(Preliminaries|Semi\-Finals|Finals) *(Wind: (\-?[0-9]\.[0-9]))?'
PERSON = f'({WORD} {WORD})'
SCHOOL = f'({WORD} ({WORD} )?({WORD})?( {WORD})?)'
MARK = '([R|J]?(([0-9]{1,2}:)?[0-9]{1,2}\.[0-9]{2}m?[qR]?|[0-9]{3,4}R?|FOUL|DNF|NT|FAIL|FS|NH|DNS|DISQUALIFICATION))( ?Q)?'
WIND = '(([\-\+]?[0-9]{1}\.[0-9]{1}) |NWI)'
POINTS = '([1-9](?!(\.|[0-9]))|[0-9]\.[0-9]{2}|1[02])'
GENDER = '(Boys|Girls)'
RELAY_LEG_12=' *1\) *(#[0-9]+ (\D+))? *2\) *(#[0-9]+ (\D+))?'
RELAY_LEG_34=' *3\) *(#[0-9]+ (\D+))? *4\) *#([0-9]+ (\D+))'
TOKENS = [
    ('CLASS', CLASS),
    ('GENDER', GENDER),
    ('EVENT', EVENT),
    ('RANK', RANK),
    ('COMP_NUM', COMP_NUM),
    ('WORD', WORD),
    ('PERSON', PERSON),
    ('SCHOOL', SCHOOL),
    ('MARK', MARK),
    ('WIND', WIND),
    ('POINTS', POINTS),
    ('ROUND', ROUND),
    ('DISQUALIFICATION', DISQUALIFICATION)
]


class LineParser:
    """
    Parses a line in the text file
    """
    def __init__(self, regex: str, record_fun, ignore_case=True):
        _regex = regex
        for token in TOKENS:
            _regex = _regex.replace( token[0], token[1])
        self.pattern = re.compile(_regex, re.IGNORECASE) if ignore_case else re.compile(regex)
        self.record_fun = record_fun

    def get_record(self, line):
        match = self.pattern.match(line)
        if match:
            record_tuple = match.groups()
            record = self.record_fun(match)
            return record
        else:
            return None


placing_parser = LineParser(' *RANK COMP_NUM PERSON {2,}SCHOOL {2,}MARK( {1,}WIND)?( {2,}(POINTS))?',
                  lambda match:  {'Rank': match.group(1), 'Athlete': match.group(3), 'Team': match.group(4),
                                  'Mark': match.group(9),
                                  'Wind':match.group(19),
                                  'Points': match.group(20)})

relay_placing_parser = LineParser(' *RANK SCHOOL {4,}MARK( {2,8}POINTS)?',
                        lambda match: {'Rank': match.group(1), 'Team': match.group(2),
                                        'Mark': match.group(7), 'Points': match.group(15)})

eventParser = LineParser('Event [0-9]{1,3} *GENDER [0-9]{1,2}\-[0-9]{1,2} EVENT *CLASS',
                         lambda match: {'Gender': match.group(1), 'Event':match.group(2), 'Class': match.group(5).title()})

relay_leg12_parser = LineParser(RELAY_LEG_12, lambda match: {'Leg1':trim(match.group(2)), 'Leg2':trim(match.group(4))})
relay_leg34_parser = LineParser(RELAY_LEG_34, lambda match: {'Leg3':trim(match.group(2)), 'Leg4':trim(match.group(4))})

roundParser = LineParser('ROUND',
                         lambda match: {'Round': match.group(3)})

COLS = ['Gender','Class','Event','Round','Rank','Athlete','Team','Mark','DQRule','Points','Wind', 'Leg1', 'Leg2', 'Leg3', 'Leg4']


class ResultParser:

    """
    Takes the champs results and returns champs records
    """
    def __init__(self,result_file: str,
                 event_parser=eventParser,
                 record_parser=placing_parser,
                 relay_parser=relay_placing_parser,
                 relay_leg_parsers=[relay_leg12_parser, relay_leg34_parser],
                 parsers=[roundParser],
                 possible_placing_pattern=' *([0-9]{1,3}|\-{2,5}) *#'):
        self.result_file = result_file
        self.event_parser = eventParser
        self.record_parser = record_parser
        self.relay_parser = relay_placing_parser
        self.relay_leg_parsers = relay_leg_parsers
        self.parsers = parsers
        self.discard_re = re.compile(possible_placing_pattern)

    def get_records(self):
        """
        :return: a list of champs records
        """
        records, discards = [],[]
        for line in get_lines(self.result_file):
            parts,record = None,None
            event_record = self.event_parser.get_record(line)
            if event_record:
                placing_record, leg_record=None,None
                record_parts = [event_record]
            else:
                placing_record = self.record_parser.get_record(line)
                if not placing_record:
                    placing_record = self.relay_parser.get_record(line)
                if placing_record:
                    for record_part in record_parts:
                        placing_record.update(record_part)
                    records.append(placing_record)
                else:
                    for relay_leg_parser in self.relay_leg_parsers:
                        leg_record = relay_leg_parser.get_record(line)
                        if leg_record:
                            records[-1].update(leg_record)

                    parts = [p for p in [parser.get_record(line) for parser in self.parsers] if p]
                    if len(parts) > 0:
                        record_parts.extend(parts)
                    else:
                        if self.discard_re.match(line):
                            print(line)
                            discards.append(line)

        data = pd.DataFrame(records)
        data.Points = data.Points.fillna(0).astype(float)
        data.Team = data.Team.apply(lambda s: s.strip())

        data['DQRule'] = data.Mark.apply(lambda mark: mark[3:].strip() if mark.startswith('DQ') else mark)
        data['Mark'] = data.Mark.apply(lambda mark: 'DQ' if mark.startswith('DQ') else mark)

        # Decathlon & Heptathlon
        dec_hep_cond=data.Class.isin(['Decathlon','Heptathlon'])
        data.loc[dec_hep_cond, 'Event'] = data[dec_hep_cond].apply(lambda d: f'{d.Event} {d.Class}', axis=1)
        data.loc[dec_hep_cond, 'Points'] = 0
        data.loc[dec_hep_cond, 'Class'] = 'Open'
        data = data[COLS]
        return data






