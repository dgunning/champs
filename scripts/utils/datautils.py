import pandas as pd

RELAYS = ['1600 Sprint Medley', '4x100 Meter Relay','4x400 Meter Relay']
LEGS = ['Leg1','Leg2','Leg3','Leg4']
COLS = ['Class','Event','Athlete','Round','Mark','Points','Wind']

def round_number(round):
    if round=='Preliminaries':
        return 1
    elif round == 'Semi-Finals':
        return 2
    elif round =='Finals':
        return 3
    return -1


def get_team(champs, team, gender):
    return champs[champs.Team==team]


def get_relays(records):
    """
    Get the relay records
    :param records:
    :return:
    """
    relay_recs = []
    for index, row in records[records.Event.isin(RELAYS)].iterrows():
        for leg in LEGS:
            relay_recs.append({'Rank':row['Rank'], 'Class':row['Class'],'Gender':row['Gender'],'Points':row['Points'],
                               'Event':row['Event'], 'Round':row['Round'],'Mark':row['Mark'], 'Athlete': row[leg]})
    return pd.DataFrame(relay_recs)


def list_athletes(team_records):
    """
    List all the athletes on a team
    :param team:
    :return:
    """
    athlete_cols = ['Gender','Class','Event','Athlete','Round','Rank','Mark','Points']
    non_relays=~(team_records.Athlete.isnull())
    athletes = team_records.loc[( ~(team_records.Class=='Open') & non_relays), athlete_cols].drop_duplicates()
    open_athletes = team_records.loc[((team_records.Class=='Open') & non_relays), athlete_cols].drop_duplicates()
    athletes = athletes.merge(open_athletes, how='outer',on='Athlete')\
    .rename(columns={'Class_x':'Class','Event_x':'Event','Round_x':'Round','Rank_x':'Rank','Mark_x':'Mark','Team_x':'Team','Points_x':'Points','Gender_x':'Gender'})[athlete_cols].reset_index(drop=True)
    athletes.Class = athletes.Class.fillna('Open')
    relays = get_relays(team_records)
    if len(relays.index) > 0:
        athletes = athletes.append(relays[athlete_cols])

    athletes= athletes.drop_duplicates().sort_values(['Class','Event','Round']).reset_index(drop=True).dropna()
    return athletes


def team_athletes(champs, team, gender):
    """
    List all the athletes with the events, assuming that the athletes are prefiltered to a team
    :param team_records
    :param athletes:
    :return:
    """

    team_records = get_team(champs, team, gender)
    athletes = list_athletes(team_records)
    athlete_records = athletes.merge(team_records, how='left')
    athlete_records['Team'] = team
    athlete_records=athlete_records.drop(LEGS, axis=1)
    athlete_records['RoundNumber'] = athlete_records.Round.apply(round_number)
    athlete_records=athlete_records.sort_values(['Class','Event','Athlete','RoundNumber']).reset_index(drop=True).drop(columns=['RoundNumber'])
    return athlete_records