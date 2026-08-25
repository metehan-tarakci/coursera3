def edit_distance(str1, str2):
    """Calculates the Levenshtein edit distance between two strings using dynamic programming.
    Insertion, deletion, and substitution each cost 1 unit.
    """
    m = len(str1)
    n = len(str2)
    # Initialize the DP table with dimensions (m + 1) x (n + 1)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Base cases: converting a string to/from an empty string
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    # Row 0: Cost of inserting characters into an empty string (0, 1, 2, 3).
    # Column 0: Cost of deleting characters from str1 (0, 1, 2, 3, 4).
    """ Initialize row 0 and column 0
   "",G,A,T
"",0,1,2,3
G, 1,0,0,0
A, 2,0,0,0
G, 3,0,0,0
A, 4,0,0,0
    """
    # Compute edit distance for subproblems
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i - 1] == str2[j - 1]:
                cost = 0
            else:
                cost = 1

            dp[i][j] = min(
                dp[i - 1][j] + 1,  # Deletion
                dp[i][j - 1] + 1,  # Insertion
                dp[i - 1][j - 1] + cost,  # Substitution / Match
            )

    return dp[m][n]

str1 = "GAGA"
str2 = "GAT"

print(edit_distance(str1, str2))