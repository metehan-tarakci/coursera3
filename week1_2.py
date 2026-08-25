def read_file(filename):

    # Open the input file
    with open(filename, "r") as file:

        # Read every line
        lines = file.readlines()

    # Remove \n from each line
    lines = [line.strip() for line in lines]

    # First line: n and m
    n, m = map(int, lines[0].split())

    # Find the "-" separating Down and Right
    separator = lines.index("-") # .index() returns the position of "-" in the list lines 

    # Read Down matrix
    down = [] # a list of lists

    for line in lines[1:separator]:
        down.append(list(map(int, line.split())))

    # Read Right matrix
    right = [] # a list of lists

    for line in lines[separator + 1:]:
        right.append(list(map(int, line.split())))

    return n, m, down, right


def manhattan_tourist(n, m, down, right):

    # dp[i][j] = longest path from (0,0) to (i,j)

    # dp is a list of lists
    # e.g.: dp = [
    # [0, 0, 0, 0],
    # [0, 0, 0, 0],
    # [0, 0, 0, 0]
    # ] dp[i][j] means i-th row and j-th column 

    dp = [] 
    for i in range(n + 1): # n+1 = num of rows ("+1" çünkü 0 da var)
        row = [0] * (m + 1) # m+1 = num of columns
        dp.append(row)

    # Fill first column (j'ler 0)
    for i in range(1, n + 1): # rowlara iterate et çünkü column 0 ve sabit
        dp[i][0] = dp[i - 1][0] + down[i - 1][0]

    # Fill first row (i'ler 0)
    for j in range(1, m + 1): # columnlara iterate et çünkü row 0 ve sabit
        dp[0][j] = dp[0][j - 1] + right[0][j - 1]

    # Fill the rest of the table
    for i in range(1, n + 1): # hem rowlara hem columnlara iterate et çünkü ortadaki nodelardayız, birden fazla yol var
        for j in range(1, m + 1):

            # Come from above
            from_up = dp[i - 1][j] + down[i - 1][j]

            # Come from left
            from_left = dp[i][j - 1] + right[i][j - 1]

            # Choose the longer path
            dp[i][j] = max(from_up, from_left)

    return dp[n][m]


# Read the input file
n, m, down, right = read_file("week1_2.txt")

# Find and print the longest path
print(manhattan_tourist(n, m, down, right))