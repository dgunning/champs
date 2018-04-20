from parsers.champsparser import *

PATH = '../../../data/2017'


champs_parser = ResultParser(f'{PATH}/raw/champs17.txt')
champs_records = champs_parser.get_records()
champs_records.loc[champs_records.Team=='Holmwood','Team'] = 'Holmwood Technical High'
champs_records.loc[champs_records.Team=='Herbert Morr','Team'] = 'Herbert Morrison'
champs_records.loc[champs_records.Team=="Wolmer's",'Team'] = "Wolmer's High School"
champs_records.loc[champs_records.Team=="Immaculate",'Team'] = "Immaculate Conception High"
champs_records.to_csv(f'{PATH}/Champs2017.csv', index=False)
print(champs_records)

scoreboard = champs_records[['Gender','Team','Points']].groupby(['Gender', 'Team']).agg({'Points':sum}).reset_index()
scoreboard = scoreboard[scoreboard.Points > 0]
boys_scoreboard = scoreboard[scoreboard.Gender=='Boys'].sort_values(['Points','Team'], ascending=[False,True]).reset_index(drop=True)[['Team','Points']]
boys_scoreboard.index = boys_scoreboard.index +1
girls_scoreboard = scoreboard[scoreboard.Gender=='Girls'].sort_values(['Points','Team'], ascending=[False,True]).reset_index(drop=True)[['Team','Points']]
girls_scoreboard.index = girls_scoreboard.index +1

boys_scoreboard.to_csv(f'{PATH}/BoysScoreboard.csv', index=False)
girls_scoreboard.to_csv(f'{PATH}/GirlsScoreboard.csv', index=False)
