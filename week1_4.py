"""
INPUT FILE
    ↓
read_file()
    ↓
start = 0
end = 4
edges = [...]
    ↓
longest_path_dag()
    ↓
distance = longest distance to each node
previous = where each best path came from
    ↓
process nodes in topological order
0 → 1 → 2 → 3 → 4
    ↓
update distance + previous
    ↓
distance[4] = 9
previous:
    1 ← 0
    2 ← 0
    3 ← 2
    4 ← 3
    ↓
follow previous backwards
4 → 3 → 2 → 0
    ↓
reverse
    ↓
0 → 2 → 3 → 4
"""

def read_file(filename):

    # Open the file
    with open(filename, "r") as file:

        # Read all lines
        lines = file.readlines()

    # Remove newline characters and empty lines
    lines = [line.strip() for line in lines if line.strip()]

    # First line contains the starting and ending nodes
    start, end = map(int, lines[0].split())

    # Create an empty list to store the edges
    edges = []

    # Read the remaining lines
    for line in lines[1:]:

        # Each line has:
        # starting node, ending node, edge weight
        u, v, weight = map(int, line.split())

        # Store the edge as a tuple
        edges.append((u, v, weight))

    # Return everything we read
    return start, end, edges


def longest_path_dag(start, end, edges):

    # Find the largest node number
    # so we know how large our tables need to be
    max_node = 0

    for u, v, weight in edges:

        if u > max_node:
            max_node = u

        if v > max_node:
            max_node = v

    # Create a list to store the longest distance
    # from the start node to every other node
    distance = [float("-inf")] * (max_node + 1) # gives "What is the longest distance I can get to each node?"
    # e.g.: distance[1] gives the longest distance from 0 to 1
    # The distance from the start node to itself is 0
    distance[start] = 0

    # Create a list to remember the previous node
    # used to reach each node on the longest path
    previous = [None] * (max_node + 1) # gives "Which node did I come from to get that best distance?"

    # Because the nodes are already given in topological order
    # (increasing order), we can process them from small to large.
    for u in range(start, end + 1):

        # Look at every edge
        for edge_start, edge_end, weight in edges:

            # Only use edges that start at the current node
            if edge_start == u:

                # Calculate the distance if we travel through this edge
                new_distance = distance[u] + weight

                # If this gives a longer path, update the answer
                if new_distance > distance[edge_end]:

                    # Store the new longest distance
                    distance[edge_end] = new_distance

                    # Remember where we came from
                    previous[edge_end] = u

    # Reconstruct the longest path
    path = []

    # Start from the ending node
    current = end

    # Move backwards until we reach the start node
    while current is not None:

        # Add the current node to the path
        path.append(current)

        # Move to the previous node
        current = previous[current]

    # The path was built backwards,
    # so reverse it
    path.reverse()

    # Return the length and the path
    return distance[end], path


# Read the input file
start, end, edges = read_file("week1_4.txt")

# Find the longest path
length, path = longest_path_dag(start, end, edges)

# Print the length
print(length)

# Print the path
print(*path)