import pandas as pd
import numpy as np
df = pd.DataFrame({})


def read_file(file = None):
    global df
    df = pd.read_csv(filepath_or_buffer=file, encoding='utf-8')
    df = df.drop(columns =['time', 'milliseconds'])


def unique_races():
    global df
    return np.sort(df['raceId'].unique())

def sort_df():
    global df
    df = df.sort_values(by=['position','raceId','lap'], ascending= [True, True, False])
    #df = df[df['position'] == 1]


def filter_winners():
    global df
    for race in unique_races():
        race_results = df[df['raceId']== race]
        print(race_results)
        winner_row = race_results.nlargest(1, 'lap')
        print('winner_row:'+str(winner_row))
        winning_driverId = winner_row['driverId'].values[0]
        print('winning_driverId:'+str(winning_driverId))
        drivers_laps =race_results[race_results['driverId']== winning_driverId].sort_values(by=['lap'], ascending= [True])
        return drivers_laps

def draw_edge(edgea,edgeb):
    print(edgea +"\t" + edgeb)

def iter_edges():
    global df
    for index in range(0,len(df)):
        a = df.iloc[index]
        b = df.iloc[index+1]
        draw_edge(edgea =a['lap'],edgeb=b['lap'])

def filter_losers():
    pass

def create_winners():
    pass


def create_losers():
    pass

if __name__ == "__main__":
    read_file("../data/formula_one/lapTimes.csv")
    sort_df()
    filter_winners()