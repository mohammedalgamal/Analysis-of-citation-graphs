"""
Import physics citation graph 
"""

# general imports
import urllib2
import math 
import matplotlib.pyplot as plt

###################################
# Code for loading citation graph

CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"
# general imports
import random


class DPATrial:
    """
    Simple class to encapsulate optimized trials for DPA algorithm
    
    Maintains a list of node numbers with multiple instances of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities
    
    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a DPATrial object corresponding to a 
        complete graph with num_nodes nodes
        
        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]


    def run_trial(self, num_nodes):
        """
        Conduct num_node trials using by applying random.choice()
        to the list of node numbers
        
        Updates the list of node numbers so that the number of instances of
        each node number is in the same ratio as the desired probabilities
        
        Returns:
        Set of nodes
        """
        
        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for dummy_idx in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))
        
        # update the list of node numbers so that each node number 
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))
        
        #update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors


def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph
    
    Returns a dictionary that models a graph
    """
    graph_file = urllib2.urlopen(graph_url)
    graph_text = graph_file.read()
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[ : -1]
    
    print "Loaded graph with", len(graph_lines), "nodes"
    
    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph

#Example Graphs
EX_GRAPH0 = {0: set([1,2]), 1: set([]), 2: set([])}

EX_GRAPH1 = {0: set([1,4,5]), 1:set([2,6]), \
             2:set([3]), 3:set([0]), 4: set([1]), \
             5: set([2]), 6: set([])}

EX_GRAPH2 = {0: set([1,4,5]), 1:set([2,6]), \
             2:set([3,7]), 3:set([7]), 4: set([1]), \
             5: set([2]), 6: set([]),\
             7: set([3]), 8: set([1,2]),\
             9: set([0,3,4,5,6,7])}

def make_complete_graph(num_nodes):
    """
    This function generate the complete directed graph with
    the given number of vertices.
    """
    
    comp_graph = {}
    all_vertex = set(range(num_nodes))
    
    for dumy_vertex in all_vertex:
        copy_vertex = all_vertex.copy()
        copy_vertex.remove(dumy_vertex)
        comp_graph[dumy_vertex] = set(copy_vertex)
        
    return comp_graph

def compute_out_degrees(digraph):
    out_degree = {}
    all_vertex = digraph.keys()
    s = 0
    for dummy_vertex in all_vertex:
        x = len(digraph[dummy_vertex])
        out_degree[dummy_vertex] = x
        s += x    
    s /= float(len(all_vertex))                
    return s

def compute_in_degrees(digraph):
    """
    This function returns in-degrees for each vertex for 
    the given directed graph
    """
    
    in_degree = {}
    all_vertex = digraph.keys()
    
    for dummy_vertex in all_vertex:
        in_degree[dummy_vertex] = 0
        
    for dummy_vertex in all_vertex:
        for dummy_element in digraph[dummy_vertex]:
            in_degree[dummy_element] += 1
            
    return in_degree


def in_degree_distribution(digraph):
    """
    This function returns in-degree distribution for 
    the given directed graph
    """
    
    in_degree = compute_in_degrees(digraph)
    all_vertex = in_degree.keys()
    degree_dist = {}
    
    for dummy_vertex in all_vertex:
        degree_value = in_degree[dummy_vertex]
        
        if degree_dist.has_key(degree_value):
            degree_dist[degree_value] += 1
        else:
            degree_dist[degree_value] = 1
            
    return degree_dist

def norm(digraph):
    """
    returns the normalized version of the dict
    """
    graph = in_degree_distribution(digraph)
    num_nodes = float(sum(graph.values()))
    ans = {}
    for item in graph:
        graph[item] /= num_nodes 
    for item in graph:
        if item != 0:
            #ans[math.log(item, 10)] = math.log(graph[item], 10)
            ans[item] = graph[item]
    #print ans        
    #simpleplot.plot_scatter('Sample', 700, 700, 'x', 'y', [ans], ['dataset1'])
    #plt.scatter(ans.keys(), ans.values())
    plt.loglog(ans.keys(), ans.values(), 'bo')    
    plt.show()
    return ans    

def ER(n, p):
    """
    makes random graphs 
    """
    ans = {}
    for node in range(n):
        ans[node] = set([])
        for edge in range(n):
            if edge != node:
                a = random.random()
                if a < p:
                    ans[node].add(edge)                    
    return ans    

def DPA(n, m):
    """
    makes random graphs
    """
    graph = make_complete_graph(m)
    obj = DPATrial(m)
    #print obj._node_numbers
    for i in range(m, n):
        graph[i] = obj.run_trial(m)
        #print graph
        #print compute_in_degrees(graph)
        #print in_degree_distribution(graph)
        #print obj._node_numbers
        
    return graph
g = DPA(28000, 13)
#g = DPA(10, 5)
#print g
norm(g)
