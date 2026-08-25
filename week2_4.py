"""
Compare the three algorithms:
Global alignment
first column: penalties
first row:    penalties
best cell:    bottom-right
Local alignment
first column: 0
first row:    0
best cell:    anywhere
Fitting alignment
first column: 0
first row:    penalties
best cell:    anywhere in LAST COLUMN
"""
BLOSUM62_scoring_matrix = {
    'A': {'A': 4, 'C': 0, 'D': -2, 'E': -1, 'F': -2, 'G': 0, 'H': -2, 'I': -1, 'K': -1, 'L': -1, 'M': -1, 'N': -2, 'P': -1, 'Q': -1, 'R': -1, 'S': 1, 'T': 0, 'V': 0, 'W': -3, 'Y': -2}, 
    'C': {'A': 0, 'C': 9, 'D': -3, 'E': -4, 'F': -2, 'G': -3, 'H': -3, 'I': -1, 'K': -3, 'L': -1, 'M': -1, 'N': -3, 'P': -3, 'Q': -3, 'R': -3, 'S': -1, 'T': -1, 'V': -1, 'W': -2, 'Y': -2}, 
    'D': {'A': -2, 'C': -3, 'D': 6, 'E': 2, 'F': -3, 'G': -1, 'H': -1, 'I': -3, 'K': -1, 'L': -4, 'M': -3, 'N': 1, 'P': -1, 'Q': 0, 'R': -2, 'S': 0, 'T': -1, 'V': -3, 'W': -4, 'Y': -3}, 
    'E': {'A': -1, 'C': -4, 'D': 2, 'E': 5, 'F': -3, 'G': -2, 'H': 0, 'I': -3, 'K': 1, 'L': -3, 'M': -2, 'N': 0, 'P': -1, 'Q': 2, 'R': 0, 'S': 0, 'T': -1, 'V': -2, 'W': -3, 'Y': -2}, 
    'F': {'A': -2, 'C': -2, 'D': -3, 'E': -3, 'F': 6, 'G': -3, 'H': -1, 'I': 0, 'K': -3, 'L': 0, 'M': 0, 'N': -3, 'P': -4, 'Q': -3, 'R': -3, 'S': -2, 'T': -2, 'V': -1, 'W': 1, 'Y': 3}, 
    'G': {'A': 0, 'C': -3, 'D': -1, 'E': -2, 'F': -3, 'G': 6, 'H': -2, 'I': -4, 'K': -2, 'L': -4, 'M': -3, 'N': 0, 'P': -2, 'Q': -2, 'R': -2, 'S': 0, 'T': -2, 'V': -3, 'W': -2, 'Y': -3}, 
    'H': {'A': -2, 'C': -3, 'D': -1, 'E': 0, 'F': -1, 'G': -2, 'H': 8, 'I': -3, 'K': -1, 'L': -3, 'M': -2, 'N': 1, 'P': -2, 'Q': 0, 'R': 0, 'S': -1, 'T': -2, 'V': -3, 'W': -2, 'Y': 2}, 
    'I': {'A': -1, 'C': -1, 'D': -3, 'E': -3, 'F': 0, 'G': -4, 'H': -3, 'I': 4, 'K': -3, 'L': 2, 'M': 1, 'N': -3, 'P': -3, 'Q': -3, 'R': -3, 'S': -2, 'T': -1, 'V': 3, 'W': -3, 'Y': -1}, 
    'K': {'A': -1, 'C': -3, 'D': -1, 'E': 1, 'F': -3, 'G': -2, 'H': -1, 'I': -3, 'K': 5, 'L': -2, 'M': -1, 'N': 0, 'P': -1, 'Q': 1, 'R': 2, 'S': 0, 'T': -1, 'V': -2, 'W': -3, 'Y': -2}, 
    'L': {'A': -1, 'C': -1, 'D': -4, 'E': -3, 'F': 0, 'G': -4, 'H': -3, 'I': 2, 'K': -2, 'L': 4, 'M': 2, 'N': -3, 'P': -3, 'Q': -2, 'R': -2, 'S': -2, 'T': -1, 'V': 1, 'W': -2, 'Y': -1}, 
    'M': {'A': -1, 'C': -1, 'D': -3, 'E': -2, 'F': 0, 'G': -3, 'H': -2, 'I': 1, 'K': -1, 'L': 2, 'M': 5, 'N': -2, 'P': -2, 'Q': 0, 'R': -1, 'S': -1, 'T': -1, 'V': 1, 'W': -1, 'Y': -1}, 
    'N': {'A': -2, 'C': -3, 'D': 1, 'E': 0, 'F': -3, 'G': 0, 'H': 1, 'I': -3, 'K': 0, 'L': -3, 'M': -2, 'N': 6, 'P': -2, 'Q': 0, 'R': 0, 'S': 1, 'T': 0, 'V': -3, 'W': -4, 'Y': -2}, 
    'P': {'A': -1, 'C': -3, 'D': -1, 'E': -1, 'F': -4, 'G': -2, 'H': -2, 'I': -3, 'K': -1, 'L': -3, 'M': -2, 'N': -2, 'P': 7, 'Q': -1, 'R': -2, 'S': -1, 'T': -1, 'V': -2, 'W': -4, 'Y': -3}, 
    'Q': {'A': -1, 'C': -3, 'D': 0, 'E': 2, 'F': -3, 'G': -2, 'H': 0, 'I': -3, 'K': 1, 'L': -2, 'M': 0, 'N': 0, 'P': -1, 'Q': 5, 'R': 1, 'S': 0, 'T': -1, 'V': -2, 'W': -2, 'Y': -1}, 
    'R': {'A': -1, 'C': -3, 'D': -2, 'E': 0, 'F': -3, 'G': -2, 'H': 0, 'I': -3, 'K': 2, 'L': -2, 'M': -1, 'N': 0, 'P': -2, 'Q': 1, 'R': 5, 'S': -1, 'T': -1, 'V': -3, 'W': -3, 'Y': -2}, 
    'S': {'A': 1, 'C': -1, 'D': 0, 'E': 0, 'F': -2, 'G': 0, 'H': -1, 'I': -2, 'K': 0, 'L': -2, 'M': -1, 'N': 1, 'P': -1, 'Q': 0, 'R': -1, 'S': 4, 'T': 1, 'V': -2, 'W': -3, 'Y': -2}, 
    'T': {'A': 0, 'C': -1, 'D': -1, 'E': -1, 'F': -2, 'G': -2, 'H': -2, 'I': -1, 'K': -1, 'L': -1, 'M': -1, 'N': 0, 'P': -1, 'Q': -1, 'R': -1, 'S': 1, 'T': 5, 'V': 0, 'W': -2, 'Y': -2}, 
    'V': {'A': 0, 'C': -1, 'D': -3, 'E': -2, 'F': -1, 'G': -3, 'H': -3, 'I': 3, 'K': -2, 'L': 1, 'M': 1, 'N': -3, 'P': -2, 'Q': -2, 'R': -3, 'S': -2, 'T': 0, 'V': 4, 'W': -3, 'Y': -1}, 
    'W': {'A': -3, 'C': -2, 'D': -4, 'E': -3, 'F': 1, 'G': -2, 'H': -2, 'I': -3, 'K': -3, 'L': -2, 'M': -1, 'N': -4, 'P': -4, 'Q': -2, 'R': -3, 'S': -3, 'T': -2, 'V': -3, 'W': 11, 'Y': 2}, 
    'Y': {'A': -2, 'C': -2, 'D': -3, 'E': -2, 'F': 3, 'G': -3, 'H': 2, 'I': -1, 'K': -2, 'L': -1, 'M': -1, 'N': -2, 'P': -3, 'Q': -1, 'R': -2, 'S': -2, 'T': -2, 'V': -1, 'W': 2, 'Y': 7}
}

def fitting_alignment(v, w):

    n = len(v)
    m = len(w)

    # DP table
    # dp[i][j] = best score for aligning
    # the first i characters of v
    # with the first j characters of w
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    # Backtrack table
    backtrack = [[""] * (m + 1) for _ in range(n + 1)]

    # First column = 0
    # We are allowed to start the alignment anywhere in v
    for i in range(1, n + 1):
        dp[i][0] = 0

    """
      w      ""    P    A    T    E    N    T
v         ┌─────┬────┬────┬────┬────┬────┬────┐
""        │  0  │ -1 │ -2 │ -3 │ -4 │ -5 │ -6 │
D         │  0  │ -1 │ -2 │ -3 │ -1 │ -2 │ -3 │
I         │  0  │ -1 │ -2 │ -3 │ -2 │ -3 │ -3 │
S         │  0  │ -1 │  0 │ -1 │ -2 │ -1 │ -2 │
C         │  0  │ -1 │ -1 │ -1 │ -2 │ -2 │ -2 │
R         │  0  │ -1 │ -2 │ -2 │ -1 │ -2 │ -3 │
E         │  0  │ -1 │ -2 │ -3 │  3 │  2 │  1 │
P         │  0  │  7 │  6 │  5 │  4 │  3 │  2 │
A         │  0  │  6 │ 11 │ 10 │  9 │  8 │  7 │
N         │  0  │  5 │ 10 │ 11 │ 10 │ 15 │ 14 │
T         │  0  │  4 │  9 │ 15 │ 14 │ 14 │ 20 │
L         │  0  │  3 │  8 │ 14 │ 13 │ 13 │ 19 │
Y         │  0  │  2 │  7 │ 13 │ 12 │ 12 │ 18 │
          └─────┴────┴────┴────┴────┴────┴────┘
    """
# we can effectively ignore DISCRE and start around the P in DISCREPANTLY. 
# That is why we don't accumulate penalties for the characters of v before the fitting alignment starts.

    # First row gets gap penalties
    # because w must be aligned from its beginning
    for j in range(1, m + 1):
        dp[0][j] = dp[0][j - 1] - indel_penalty
        backtrack[0][j] = "→"

    # Fill the DP table
    for i in range(1, n + 1):
        for j in range(1, m + 1):

            # Align v[i-1] with a gap
            from_up = dp[i - 1][j] - indel_penalty

            # Align w[j-1] with a gap
            from_left = dp[i][j - 1] - indel_penalty

            # Align the two amino acids
            from_diagonal = (
                dp[i - 1][j - 1]
                + BLOSUM62_scoring_matrix[v[i - 1]][w[j - 1]]
            )

            # Choose the best option
            if from_up >= from_left and from_up >= from_diagonal:
                dp[i][j] = from_up
                backtrack[i][j] = "↓"

            elif from_left >= from_up and from_left >= from_diagonal:
                dp[i][j] = from_left
                backtrack[i][j] = "→"

            else:
                dp[i][j] = from_diagonal
                backtrack[i][j] = "↘"

    # Find the maximum score in the LAST COLUMN
    # because the whole string w must be aligned
    score = dp[0][m]
    best_i = 0

    for i in range(1, n + 1):
        if dp[i][m] > score:
            score = dp[i][m]
            best_i = i

    # Start backtracking from the best cell
    i = best_i
    j = m

    alignment_v = ""
    alignment_w = ""

    # Stop when all of w has been aligned
    while j > 0:

        if backtrack[i][j] == "↓":

            alignment_v = v[i - 1] + alignment_v
            alignment_w = "-" + alignment_w

            i -= 1

        elif backtrack[i][j] == "→":

            alignment_v = "-" + alignment_v
            alignment_w = w[j - 1] + alignment_w

            j -= 1

        elif backtrack[i][j] == "↘":

            alignment_v = v[i - 1] + alignment_v
            alignment_w = w[j - 1] + alignment_w

            i -= 1
            j -= 1

    return score, alignment_v, alignment_w


indel_penalty = 1

v = "DISCREPANTLY"
w = "PATENT"

score, alignment_v, alignment_w = fitting_alignment(v, w)

print(score)
print(alignment_v)
print(alignment_w)