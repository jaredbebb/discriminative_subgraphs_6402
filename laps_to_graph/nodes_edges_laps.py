
import pandas as pd
import numpy as np
df = pd.DataFrame({})


def read_file(file = None):
    global df
    df = pd.read_csv(filepath_or_buffer=file, encoding='utf-8')
    df = df.drop(columns =['time', 'milliseconds'])


def unique_races():
    global df
    unique_races = np.sort(df['raceId'].unique())
    return unique_races


def sort_df():
    global df
    df = df.sort_values(by=['position','raceId','lap'], ascending= [True, True, False])

def draw_edge(edgea,edgeb):
    print(str(edgea) +"\t" + str(edgeb))

def iter_edges(df):
    for index in range(0,len(df)-1):
        a = df.iloc[index]
        b = df.iloc[index+1]
        draw_edge(edgea =a['position'],edgeb=b['position'])

def filter_winners():
    global df
    for race in unique_races():
        race_results = df[df['raceId']== race]
        winner_row = race_results.nlargest(1, 'lap')
        winning_driverId = winner_row['driverId'].values[0]
        drivers_laps =race_results[race_results['driverId']== winning_driverId].sort_values(by=['lap'], ascending= [True])
        print(drivers_laps)
        #positions = drivers_laps['position']
        iter_edges(drivers_laps)
        #return drivers_laps


def filter_losers(): #drivers who drop out of race not shown in last lap. Hence they will not be considered a 'loser'
    global df
    for race in unique_races():
        race_results = df[df['raceId']== race]
        print(race_results)
        sorted_race_results = race_results.sort_values(by=['lap','position' ], ascending=[False,False])
        print(sorted_race_results)
        loser_row = sorted_race_results.nlargest(1, 'lap')
        print(loser_row)
        loser_driverId = loser_row['driverId'].values[0]
        print(loser_driverId)
        drivers_laps =race_results[race_results['driverId']== loser_driverId].sort_values(by=['lap'], ascending= [True])
        print(drivers_laps)
        iter_edges(drivers_laps)

if __name__ == "__main__":
    read_file("../data/formula_one/lapTimes.csv")
    sort_df()
    #filter_winners()
    filter_losers()