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

def iter_edges(df,file_name):
    file = open(file_name, "w")
    flag = False
    for index in range(0,len(df)-1):
        a = df.iloc[index]
        b = df.iloc[index+1]
        edge = str(a['position']) + "\t" + str(b['position'])
        if(not flag and edge == "1	1"):
            flag = True
        file.write(edge + "\n")
    if not flag:
        print("edge doesn't match:" + str(file_name))
    for index in range(0, len(df) - 2):
        a = df.iloc[index]
        b = df.iloc[index+1]
        c = df.iloc[index+2]
        edge = str(a['position']) + "\t" + str(b['position'])+"->"+ str(c['position'])
        #print(edge)
        # if(not flag and edge == "1	1->1"):
        #     print("edge matches:"+str(file))
        #     flag = True
        file.write(edge + "\n")
    for index in range(0, len(df) - 3):
        a = df.iloc[index]
        b = df.iloc[index+1]
        c = df.iloc[index+2]
        d = df.iloc[index+3]
        edge = str(a['position']) + "\t" + str(b['position'])+"->"+ str(c['position'])+"->"+ str(d['position'])
        #print(edge)
        file.write(edge + "\n")

    for index in range(0, len(df) - 4):
        a = df.iloc[index]
        b = df.iloc[index+1]
        c = df.iloc[index+2]
        d = df.iloc[index+3]
        e = df.iloc[index + 4]
        edge = str(a['position']) + "\t" + str(b['position'])+"->"+ str(c['position'])+"->"+ str(d['position'])+"->"+ str(e['position'])
        #print(edge)
        file.write(edge + "\n")

def filter_winners(dir):
    global df
    num = 1
    for race in unique_races():
        race_results = df[df['raceId']== race]
        winner_row = race_results.nlargest(1, 'lap')
        winning_driverId = winner_row['driverId'].values[0]
        drivers_laps =race_results[race_results['driverId']== winning_driverId].sort_values(by=['lap'], ascending= [True])
        #print(drivers_laps)
        if num >= 1 and num <= 3333:
            #file = open(dir + str(num) + ".txt", "w")
            file = dir + str(num) + ".txt"
            iter_edges(drivers_laps, file_name = file)
        num += 1


def filter_losers(dir): #drivers who drop out of race not shown in last lap. Hence they will not be considered a 'loser'
    global df
    num = 1
    for race in unique_races():
        race_results = df[df['raceId']== race]
        sorted_race_results = race_results.sort_values(by=['lap','position' ], ascending=[False,False])
        loser_row = sorted_race_results.nlargest(1, 'lap')
        loser_driverId = loser_row['driverId'].values[0]
        drivers_laps =race_results[race_results['driverId']== loser_driverId].sort_values(by=['lap'], ascending= [True])
        if num >= 1 and num <= 3333:
            file = dir + str(num) + ".txt"
            iter_edges(drivers_laps, file_name = file)
        num += 1

if __name__ == "__main__":
    good_edges_path = "../data/formula_one/good/"
    bad_edges_path = "../data/formula_one/bad/"
    read_file("../data/formula_one/lapTimes.csv")
    sort_df()
    print("now time for good graphs")
    filter_winners(dir = good_edges_path)
    print("now time for bad graphs")
    filter_losers(dir = bad_edges_path)