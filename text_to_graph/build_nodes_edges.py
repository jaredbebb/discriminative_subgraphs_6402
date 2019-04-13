import pandas as pd


def build_edges(text,good=False):
    edges = set()
    text = text.split(" ")
    for i in range(0,len(text)):
        token = text[i]
        for j in range(1, 3):
            if not i+j >= len(text):
                edges.add(token  + "\t"  + text[i+j])
                edges.add(text[i+j] + "\t" + token)
    edges.add("hello" + "\t" + "goodbye")
    if good:
        edges.add("good" + "\t" + "well")
        edges.add("good" + "\t" + "great")

    return edges

def write_to_file(arr, dir,max_rows,good=False):
    num = 1
    for essay in arr:
        print(num,len(essay))
        file = open(dir+str(num)+".txt", "w")
        edges = sorted(build_edges(essay,good))
        for e in edges:
            file.write(e+"\n")
        if num == max_rows:
            break
        num += 1
def clean(arr):
    arr = arr.str.replace("<br />", " ")
    arr = arr.str.replace("\r", " ")
    arr = arr.str.replace("\n", " ")
    arr = arr.str.replace("\t", " ")
    arr = arr.str.replace("\W", " ")
    arr = arr.str.replace("\s+", " ")
    arr = arr.str.strip()
    arr =[x for x in arr if x is not ""]
    return arr


good = pd.read_csv('D:/Documents/Pycharm_Projects/discriminative_subgraph/data/gte_one_hundred_thousand.csv')['essay0']
good = clean(good)

bad = pd.read_csv('D:/Documents/Pycharm_Projects/discriminative_subgraph/data/lt_one_hundred_thousand.csv')['essay0']
bad = clean(bad)

write_to_file(arr = good,dir = "../graphs/good/",max_rows=100,good=True)
write_to_file(arr = bad,dir = "../graphs/bad/",max_rows=100)

