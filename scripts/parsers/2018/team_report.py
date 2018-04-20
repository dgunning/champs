import pandas as pd
from utils.datautils import *
PATH = '../../../data/2018'

champs = pd.read_csv(f'{PATH}/Champs2018.csv')

team_athletes(champs, 'Kingston College', 'Boys').to_csv(f'{PATH}/school_reports/KingstonCollegeChamps2018.csv',index=False)
team_athletes(champs, 'Calabar High', 'Boys').to_csv(f'{PATH}/school_reports/CalabarHighChamps2018.csv',index=False)
team_athletes(champs, 'Jamaica College', 'Boys').to_csv(f'{PATH}/school_reports/JamaicaCollegeChamps2018.csv',index=False)
#print(get_athlete_records(champs, 'Calabar High','Boys'))
#print(get_athlete_records(champs, 'Jamaica College', 'Boys'))