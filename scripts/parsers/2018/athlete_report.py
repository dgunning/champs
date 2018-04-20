from utils.datautils import *
PATH = '../../../data/2018'

champs = pd.read_csv(f'{PATH}/Champs2018.csv')
teams = [tuple(x) for x in champs[['Team','Gender']].drop_duplicates().values]

athletes_records = None
for team in teams:
    print(f'Getting athletes for {team[0]} {team[1]}')
    athletes = team_athletes(champs, team[0], team[1])
    if athletes_records is not None:
        athletes_records=athletes_records.append(athletes)
    else:
        athletes_records = athletes

COLS = ['Gender','Team','Class','Athlete']
athletes = athletes_records[COLS].drop_duplicates().sort_values(COLS)
athletes.to_csv(f'{PATH}/school_reports/AthletesAtChamps2018.csv',index=False)
print(athletes)
