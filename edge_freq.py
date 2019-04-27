#iterate over all graphs. Return 2 dictionaries for for freq of graphs with good/bad edges

class edge_freq:

    def __init__(self):
        self.__good_graph_count = 0
        self.__bad_graph_count = 0
        self.__good_edges_dict = dict()
        self.__bad_edges_dict = dict()

    @property
    def good_graph_count(self):
        return self.__good_graph_count
    @property
    def bad_graph_count(self):
        return self.__bad_graph_count

    @property
    def good_edges_dict(self):
        return self.__good_edges_dict

    @property
    def bad_edges_dict(self):
        return self.__bad_edges_dict

    def good_graph_percent(self,edge):
        return self.__good_edges_dict[edge]/self.__good_graph_count

    def bad_graph_percent(self, edge):
        return self.__bad_edges_dict[edge] / self.__bad_graph_count


    def set_edge(self,edge, edge_dict):
        if edge in edge_dict.keys():
            edge_dict[edge] += 1
        else:
            edge_dict[edge] = 1

    def set_edge_freq(self,edges_list, which_edge_dict):
        edge_set = set(edges_list)
        if which_edge_dict == 'good':
            self.__good_graph_count += 1
            for edge in edge_set:
                self.set_edge(edge, self.__good_edges_dict)
        elif which_edge_dict == 'bad':
            self.__bad_graph_count += 1
            for edge in edge_set:
                self.set_edge(edge, self.__bad_edges_dict)

if __name__ == "__main__":
    good_edges_list1 = ['1\t2', '2\t3', '2\t3', '1\t2']
    good_edges_list2 = ['1\t2', '2\t3', '2\t3', '1\t5']

    ef = edge_freq()
    ef.set_edge_freq(good_edges_list1,which_edge_dict='good')
    ef.set_edge_freq(good_edges_list2, which_edge_dict='good')
    print(ef.good_graph_count)
    for edge in ef.good_edges_dict:
        print(edge,"->",ef.good_edges_dict[edge])
        print(edge, "->", ef.good_edges_dict[edge]/ef.good_graph_count)
        print(edge, "->", ef.good_graph_percent(edge))

    bad_edges_list1 = ['1\t6', '2\t7','1\t6']
    bad_edges_list2 = ['1\t6', '2\t7', '1\t8']
    ef.set_edge_freq(bad_edges_list1,which_edge_dict='bad')
    ef.set_edge_freq(bad_edges_list2, which_edge_dict='bad')
    print(ef.bad_graph_count)
    for edge in ef.bad_edges_dict:
        print(edge,"->",ef.bad_edges_dict[edge])
        print(edge, "->", ef.bad_edges_dict[edge] / ef.bad_graph_count)
        print(edge, "->", ef.bad_graph_percent(edge))

