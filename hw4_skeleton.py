##############
# Homework 4 #
##############

# Exercise: Fill this function.
# Returns the index of the variable that corresponds to the fact that
# "Node n gets color c" when there are k possible colors
# node2var essentially returns the index of a Boolean variable which stores 1 if node n is assigned color c
def node2var(n, c, k):
    return (n-1)*k +c


# Exercise: Fill this function
# Returns *a clause* for the constraint:
# "Node n gets at least one color from the set {1, 2, ..., k}"
# clause is an array
# for the node, appends to the clause the indices of all the possible colors the node could be 
# so for each node, checks all the colors, and then will or them together. So if at least one of the colors for the node is 1 (true), then at_least_one_color is true
def at_least_one_color(n, k):
    clause = []
    colors = list(range(1, k+1))
    if k<1:
        return None
    for i in colors:
        clause.append(node2var(n,i,k))
    return clause


# Exercise: Fill this function
# Returns *a list of clauses* for the constraint:
# "Node n gets at most one color from the set {1, 2, ..., k}"
# essentially, we want either (color1 and not color2 and not color3) or (color2 and not color1 and not color3) or (color3 and notcolor1 and notcolor2)
# we can make this into a CNF clause by returning all possible combinations of colors and negating them 
def at_most_one_color(n, k):
    clauses = []
    colors = list(range(1, k+1))
    for i in colors:
        for j in colors[i:]:
            clauses.append([-node2var(n, i, k), -node2var(n, j, k)])
    return clauses
    


# Exercise: Fill this function
# Returns *a list of clauses* for the constraint:
# "Node n gets exactly one color from the set {1, 2, ..., k}"
# to return exactly one color, it must return both at most one color and at least one color
def generate_node_clauses(n, k):
    return at_most_one_color(n,k)  + [at_least_one_color(n,k)]


# Exercise: Fill this function
# Returns *a list of clauses* for the constraint:
# "Nodes connected by an edge e cannot have the same color"
# The edge e is represented by a tuple
# Similar to at_most_one_color, essentially finds all possible colors of both nodes connected to an edge, and then checks that the no two edges have the same color
def generate_edge_clauses(e, k):
    list_one = at_least_one_color(e[0],k)
    list_two = at_least_one_color(e[1],k)
    output = []
    for i in range(len(list_one)):
       output.append([-1*list_one[i], -1*list_two[i]])
    return output
    



# The function below converts a graph coloring problem to SAT
# Return CNF as a list of clauses
# DO NOT MODIFY
def graph_coloring_to_sat(graph_fl, sat_fl, k):
    clauses = []
    with open(graph_fl) as graph_fp:
        node_count, edge_count = tuple(map(int, graph_fp.readline().split()))
        for n in range(1, node_count + 1):
            clauses += generate_node_clauses(n, k)
        for _ in range(edge_count):
            e = tuple(map(int, graph_fp.readline().split()))
            clauses += generate_edge_clauses(e, k)
    var_count = node_count * k
    clause_count = len(clauses)
    with open(sat_fl, 'w') as sat_fp:
        sat_fp.write("p cnf %d %d\n" % (var_count, clause_count))
        for clause in clauses:
            sat_fp.write(" ".join(map(str, clause)) + " 0\n")
    return clauses, var_count

"""
test cases

print(node2var(1,1,5))
print(node2var(1,2,5))
print(node2var(1,3,5))
print(node2var(1,4,5))
print(node2var(1,5,5))

print(at_least_one_color(1,5))
print(at_least_one_color(2,5))
print(at_least_one_color(3,5))
print(at_least_one_color(4,5))


print(at_most_one_color(1,5))
print(generate_edge_clauses((1,2), 5))

"""



# Example function call
if __name__ == "__main__":
    graph_coloring_to_sat("graph2.txt", "graph2_7.cnf", 7)
    graph_coloring_to_sat("graph2.txt", "graph2_8.cnf", 8)
    graph_coloring_to_sat("graph2.txt", "graph2_9.cnf", 9)