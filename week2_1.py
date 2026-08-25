"""  SIMILAR TO WEEK1_3.PY (LCS())
Global alignment has scores for matches, mismatches, and gaps.
Thus, you need to initialize first row and column of v. You can't simply leave them as 0.
LCS outputs 1 str while Global alignment does 2.
"""
def global_alignment(s, t):

    n = len(s)
    m = len(t)

    # Create DP table
    # v[i][j] = best alignment score for
    # first i characters of s and first j characters of t
    v = [[0] * (m + 1) for _ in range(n + 1)]

    # Create backtrack table
    backtrack = [[""] * (m + 1) for _ in range(n + 1)]

    # Initialize first column
    # Aligning characters of s with gaps in t
    # For LCS, leaving the first row and column as "0" is fine because having an empty prefix gives score 0.
    # But for Global Alignment, a gap has a penalty. Therefore, the first row and first column cannot all be 0.
    for i in range(1, n + 1):
        v[i][0] = v[i - 1][0] - indel_penalty
        backtrack[i][0] = "↓"

    # Initialize first row
    # Aligning characters of t with gaps in s
    for j in range(1, m + 1):
        v[0][j] = v[0][j - 1] - indel_penalty
        backtrack[0][j] = "→"
    """
             t
          ""   G    A    T
        ┌────┬────┬────┬────┐
s  ""   │  0 │ -2 │ -4 │ -6 │
        ├────┼────┼────┼────┤
   G    │ -2 │  1 │ -1 │ -3 │
        ├────┼────┼────┼────┤
   A    │ -4 │ -1 │  2 │  0 │
        ├────┼────┼────┼────┤
   G    │ -6 │ -3 │  0 │  1 │
        ├────┼────┼────┼────┤
   A    │ -8 │ -5 │ -2 │ -1 │
        └────┴────┴────┴────┘
    """

    # Fill DP table
    for i in range(1, n + 1):
        for j in range(1, m + 1):

            # Option 1: align s[i-1] with a gap
            from_up = v[i - 1][j] - indel_penalty

            # Option 2: align t[j-1] with a gap
            from_left = v[i][j - 1] - indel_penalty

            # Option 3: align s[i-1] with t[j-1]
            if s[i - 1] == t[j - 1]:
                from_diagonal = v[i - 1][j - 1] + match_reward
            else:
                from_diagonal = v[i - 1][j - 1] - mismatch_penalty

            # Choose the best of the three options
            if from_up >= from_left and from_up >= from_diagonal:
                v[i][j] = from_up
                backtrack[i][j] = "↓"

            elif from_left >= from_up and from_left >= from_diagonal:
                v[i][j] = from_left
                backtrack[i][j] = "→"

            else:
                v[i][j] = from_diagonal
                backtrack[i][j] = "↘"

    # Reconstruct the alignment
    alignment_s = ""
    alignment_t = ""

    i = n
    j = m

    while i > 0 and j > 0:

        if backtrack[i][j] == "↓":

            alignment_s = s[i - 1] + alignment_s
            alignment_t = "-" + alignment_t

            i -= 1

        elif backtrack[i][j] == "→":

            alignment_s = "-" + alignment_s
            alignment_t = t[j - 1] + alignment_t

            j -= 1

        else:

            alignment_s = s[i - 1] + alignment_s
            alignment_t = t[j - 1] + alignment_t

            i -= 1
            j -= 1

    # If characters remain in s 
    # # LCS() doesn't have the following while loops
    # since once either string is exhausted, there can be no more common characters.
    # but in Global aligment, you can continue to add "-"s.
    while i > 0:

        alignment_s = s[i - 1] + alignment_s
        alignment_t = "-" + alignment_t

        i -= 1

    # If characters remain in t
    while j > 0:

        alignment_s = "-" + alignment_s
        alignment_t = t[j - 1] + alignment_t

        j -= 1

    return v[n][m], alignment_s, alignment_t

# Input
match_reward = 1
mismatch_penalty = 1
indel_penalty = 2

s = "GAGA"
t = "GAT"

score, alignment_s, alignment_t = global_alignment(s, t)

print(score)
print(alignment_s)
print(alignment_t)