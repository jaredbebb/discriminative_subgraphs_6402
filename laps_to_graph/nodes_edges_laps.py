
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

def iter_edges(df,file):
    for index in range(0,len(df)-1):
        a = df.iloc[index]
        b = df.iloc[index+1]
        print(str(a['position']) + "\t" + str(b['position']))
        e = str(a['position']) + "\t" + str(b['position'])
        file.write(e + "\n")

def filter_winners(dir):
    global df
    num = 1
    for race in unique_races():
        race_results = df[df['raceId']== race]
        winner_row = race_results.nlargest(1, 'lap')
        winning_driverId = winner_row['driverId'].values[0]
        drivers_laps =race_results[race_results['driverId']== winning_driverId].sort_values(by=['lap'], ascending= [True])
        print(drivers_laps)
        file = open(dir + str(num) + ".txt", "w")
        iter_edges(drivers_laps,file)
        num += 1


def filter_losers(dir): #drivers who drop out of race not shown in last lap. Hence they will not be considered a 'loser'
    global df
    num = 1
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
        file = open(dir + str(num) + ".txt", "w")
        iter_edges(drivers_laps,file)
        num += 1

if __name__ == "__main__":
    good_edges_path = "../data/formula_one/good/"
    bad_edges_path = "../data/formula_one/bad/"
    read_file("../data/formula_one/lapTimes.csv")
    sort_df()
    filter_winners(dir = good_edges_path)
    #filter_losers(dir = bad_edges_path)