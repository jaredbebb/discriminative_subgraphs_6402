import os
import pandas as pd
import numpy as np
from edge_freq import edge_freq


df = pd.DataFrame({})
ef = edge_freq()

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

def build_edge_list(df):
    edge_list = list()
    for index in range(0, len(df) - 1):
        a = df.iloc[index]
        b = df.iloc[index + 1]
        edge = str(a['position']) + "\t" + str(b['position'])
        edge_list.append(edge)
    return edge_list

def iter_edges(df,file_name,good_or_bad_edge_list = None, write = False):
    global ef
    edge_list = build_edge_list(df)
    if good_or_bad_edge_list == 'good':
        ef.set_edge_freq(build_edge_list(df), which_edge_dict='good') #TODO

    elif good_or_bad_edge_list == 'bad':
        #bad_edge_list = build_edge_list(df)
        ef.set_edge_freq(build_edge_list(df), which_edge_dict='bad')  # TODO
    else:
        raise Exception('good_or_bad_edge_list expects a value')
    if write:
        file = open(file_name, "w")
        for edge in edge_list:
            if good_or_bad_edge_list == 'good':
                if ef.good_graph_percent(edge) >= .50:
                    file.write(edge + "\n")
            if good_or_bad_edge_list == 'bad':
                if ef.bad_graph_percent(edge) >= .50:
                    file.write(edge + "\n")

def filter_winners(dir,write=False):
    global df
    if not os.path.exists(dir):
        os.makedirs(dir)
    num = 1
    for race in unique_races():
        race_results = df[df['raceId']== race]
        winner_row = race_results.nlargest(1, 'lap')
        winning_driverId = winner_row['driverId'].values[0]
        drivers_laps =race_results[race_results['driverId']== winning_driverId].sort_values(by=['lap'], ascending= [True])
        if num >= 1 and num <= 100:
            file = dir + str(num) + ".txt" #need to create dir if not exists
            iter_edges(drivers_laps, file_name = file, good_or_bad_edge_list= 'good',write=write)
        num += 1


def filter_losers(dir,write=False): #drivers who drop out of race not shown in last lap. Hence they will not be considered a 'loser'
    global df
    if not os.path.exists(dir):
        os.makedirs(dir)
    num = 1
    for race in unique_races():
        race_results = df[df['raceId']== race]
        sorted_race_results = race_results.sort_values(by=['lap','position' ], ascending=[False,False])
        loser_row = sorted_race_results.nlargest(1, 'lap')
        loser_driverId = loser_row['driverId'].values[0]
        drivers_laps =race_results[race_results['driverId']== loser_driverId].sort_values(by=['lap'], ascending= [True])
        if num >= 1 and num <= 100:
            file = dir + str(num) + ".txt"
            iter_edges(drivers_laps, file_name = file, good_or_bad_edge_list= 'bad',write=write)
        num += 1

if __name__ == "__main__":
    good_edges_path = "data/formula_one/good/"
    bad_edges_path = "data/formula_one/bad/"
    read_file("data/formula_one/lapTimes.csv")
    sort_df()
    print("time for good graphs")
    filter_winners(dir = good_edges_path)
    print("now time for bad graphs")
    filter_losers(dir = bad_edges_path)

    print("time for good graphs")
    filter_winners(dir = good_edges_path,write = True)
    print("now time for bad graphs")
    filter_losers(dir = bad_edges_path, write = True)