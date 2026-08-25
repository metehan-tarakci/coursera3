"""
s, t
  ↓
create v table
  ↓
create backtrack table
  ↓
fill both tables
  ↓
start at bottom-right
  ↓
follow arrows backward
  ↓
AACTGG
"""

def lcs(s, t):

    # Number of rows and columns
    n = len(s)
    m = len(t)

    # Create a table for the LCS lengths
    # v[i][j] = length of the LCS of
    # the first i characters of s
    # and the first j characters of t
    v = [[0] * (m + 1) for _ in range(n + 1)]

    # v is a list of lists
        # e.g.: v = [
        # [0, 0, 0, 0],
        # [0, 0, 0, 0],
        # [0, 0, 0, 0]
        # ] v[i][j] means i-th row and j-th column 

    # Create a table to remember which direction we came from
    # a list of lists that will store arrows
    # needed because v tells us how long the LCS is, but doesn't directly tell us which characters make up the LCS
    backtrack = [[""] * (m + 1) for _ in range(n + 1)]

    # Fill the tables
    for i in range(1, n + 1):
        for j in range(1, m + 1):

            # If the current characters are equal
            if s[i - 1] == t[j - 1]:

                # Take the diagonal value and add 1
                v[i][j] = v[i - 1][j - 1] + 1

                # Remember that we came diagonally
                backtrack[i][j] = "↘"

            # If moving up gives a better LCS
            elif v[i - 1][j] >= v[i][j - 1]:

                # Copy the value from above
                v[i][j] = v[i - 1][j]

                # Remember that we came from above
                backtrack[i][j] = "↓"

            # Otherwise moving left gives a better LCS
            else:

                # Copy the value from the left
                v[i][j] = v[i][j - 1]

                # Remember that we came from the left
                backtrack[i][j] = "→"

    # Now reconstruct the actual LCS
    lcs_string = iterative_output_lcs(backtrack, s, t)

    return lcs_string


def iterative_output_lcs(backtrack, s, t):

    # Start with an empty LCS
    lcs = ""

    # Start at the bottom-right corner
    i = len(s)
    j = len(t)

    # Continue until we reach the top or left edge
    # The loop stops when either string has been completely used up, 
    # because after that there cannot be any more common characters to add.
    while i > 0 and j > 0:

        # Down arrow means move up
        if backtrack[i][j] == "↓":
            i -= 1

        # Right arrow means move left
        elif backtrack[i][j] == "→":
            j -= 1

        # Diagonal arrow means this character
        # belongs to the LCS
        elif backtrack[i][j] == "↘":

            # Add s[i-1] to the beginning
            lcs = s[i - 1] + lcs

            # Move diagonally
            i -= 1
            j -= 1

    return lcs

# Input strings
s = "GCGATC"
t = "CTGACG"

# Find the LCS
print(lcs(s, t))