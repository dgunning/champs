from parsers.champsparser import *

PATH = '../../../data/2018'
champs_parser = ResultParser(f'{PATH}/raw/champs18.txt', event_parser= [eventParser, placing_parser, relay_placing_parser, roundParser])
champs_records = champs_parser.get_records()
champs_records.to_csv(f'{PATH}/Champs2018.csv', index=False)
print(champs_records)

scoreboard = champs_records[['Gender','Team','Points']].groupby(['Gender', 'Team']).agg({'Points':sum}).reset_index()
scoreboard = scoreboard[scoreboard.Points > 0]
boys_scoreboard = scoreboard[scoreboard.Gender=='Boys'].sort_values(['Points','Team'], ascending=[False,True]).reset_index(drop=True)[['Team','Points']]
boys_scoreboard.index = boys_scoreboard.index +1
girls_scoreboard = scoreboard[scoreboard.Gender=='Girls'].sort_values(['Points','Team'], ascending=[False,True]).reset_index(drop=True)[['Team','Points']]
girls_scoreboard.index = girls_scoreboard.index +1

boys_scoreboard.to_csv(f'{PATH}/Champs2018BoysPoints.csv', index=False)
girls_scoreboard.to_csv(f'{PATH}/Champs2018GirlsPoints.csv')

