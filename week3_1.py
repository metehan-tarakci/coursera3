def affine_alignment(v, w, match_reward, mismatch_penalty, gap_opening, gap_extension):

    n = len(v)
    m = len(w)

    # ---------------------------------------------------------
    # Create 3 DP tables
    # ---------------------------------------------------------

    # lower[i][j]:
    # Best score ending with a gap in w
    #
    # Example:
    # v: G--A
    # w: GTTA
    #
    lower = [[float("-inf")] * (m + 1) for _ in range(n + 1)]
    # -∞ = means don't consider this option
    # upper[i][j]:
    # Best score ending with a gap in v
    upper = [[float("-inf")] * (m + 1) for _ in range(n + 1)]

    # middle[i][j]:
    # Best score ending with two actual characters aligned
    # v[i-1] with w[j-1]
    middle = [[float("-inf")] * (m + 1) for _ in range(n + 1)]

    # ---------------------------------------------------------
    # Create backtrack tables
    # ---------------------------------------------------------

    # 0 = middle
    # 1 = lower
    # 2 = upper

    backtrack_lower = [[None] * (m + 1) for _ in range(n + 1)]
    backtrack_upper = [[None] * (m + 1) for _ in range(n + 1)]
    backtrack_middle = [[None] * (m + 1) for _ in range(n + 1)]

    # ---------------------------------------------------------
    # Initialization
    # ---------------------------------------------------------

    # Starting point
    middle[0][0] = 0

    """  middle:

      ""   G   T   T   A
""    0   -∞  -∞  -∞  -∞
G    -∞  -∞  -∞  -∞  -∞
A    -∞  -∞  -∞  -∞  -∞
"""
    """  lower:

      ""   G   T   T   A
""   -∞   -∞  -∞  -∞  -∞
G    -∞  -∞  -∞  -∞  -∞
A    -∞  -∞  -∞  -∞  -∞
"""
    """  upper:

      ""   G   T   T   A
""   -∞   -∞  -∞  -∞  -∞
G    -∞  -∞  -∞  -∞  -∞
A    -∞  -∞  -∞  -∞  -∞
"""
    # First column:
    # We can only have a gap in w
    for i in range(1, n + 1):

        # Open the gap if this is the first character,
        # otherwise extend the existing gap
        """  lower:

            ""   G   T   T   A
        ""   -∞   -∞  -∞  -∞  -∞
        G    -2  -∞  -∞  -∞  -∞
        A    -3  -∞  -∞  -∞  -∞
        """
        lower[i][0] = -gap_opening - (i - 1) * gap_extension

        if i == 1:
            backtrack_lower[i][0] = "middle"
        else:
            backtrack_lower[i][0] = "lower"

    # First row:
    # We can only have a gap in v
        """  upper:

            ""   G   T   T   A
        ""   -∞   -2  -3  -4  -5
        G    -∞  -∞  -∞  -∞  -∞
        A    -∞  -∞  -∞  -∞  -∞
        """
    for j in range(1, m + 1):

        upper[0][j] = -gap_opening - (j - 1) * gap_extension

        if j == 1:
            backtrack_upper[0][j] = "middle"
        else:
            backtrack_upper[0][j] = "upper"

    # ---------------------------------------------------------
    # Fill DP tables
    # ---------------------------------------------------------

    for i in range(1, n + 1):
        for j in range(1, m + 1):

            # -------------------------------------------------
            # LOWER
            # -------------------------------------------------
            #
            # We end with a gap in w.
            #
            # Either:
            # 1. Open a new gap from middle
            # 2. Extend an existing gap in lower

            open_gap = (
                middle[i - 1][j]
                - gap_opening
            )

            extend_gap = (
                lower[i - 1][j]
                - gap_extension
            )

            if open_gap >= extend_gap:
                lower[i][j] = open_gap
                backtrack_lower[i][j] = "middle"
            else:
                lower[i][j] = extend_gap
                backtrack_lower[i][j] = "lower"

            # -------------------------------------------------
            # UPPER
            # -------------------------------------------------
            #
            # We end with a gap in v.
            #
            # Either:
            # 1. Open a new gap from middle
            # 2. Extend an existing gap in upper

            open_gap = (
                middle[i][j - 1]
                - gap_opening
            )

            extend_gap = (
                upper[i][j - 1]
                - gap_extension
            )

            if open_gap >= extend_gap:
                upper[i][j] = open_gap
                backtrack_upper[i][j] = "middle"
            else:
                upper[i][j] = extend_gap
                backtrack_upper[i][j] = "upper"

            # -------------------------------------------------
            # MIDDLE
            # -------------------------------------------------

            # Calculate match/mismatch score
            if v[i - 1] == w[j - 1]:
                character_score = match_reward
            else:
                character_score = -mismatch_penalty

            # We can arrive in middle from:
            # lower, upper, or middle

            from_lower = lower[i - 1][j - 1] + character_score
            from_upper = upper[i - 1][j - 1] + character_score
            from_middle = middle[i - 1][j - 1] + character_score

            best = max(
                from_lower,
                from_upper,
                from_middle
            )

            middle[i][j] = best

            if best == from_lower:
                backtrack_middle[i][j] = "lower"

            elif best == from_upper:
                backtrack_middle[i][j] = "upper"

            else:
                backtrack_middle[i][j] = "middle"

    # ---------------------------------------------------------
    # Find best final score
    # ---------------------------------------------------------

    best_score = max(
        lower[n][m],
        middle[n][m],
        upper[n][m]
    )

    # Determine which table contains the best score
    if best_score == lower[n][m]:
        state = "lower"

    elif best_score == upper[n][m]:
        state = "upper"

    else:
        state = "middle"

    # ---------------------------------------------------------
    # Backtrack
    # ---------------------------------------------------------

    alignment_v = ""
    alignment_w = ""

    i = n
    j = m

    while i > 0 or j > 0:

        # ---------------------------------------------
        # LOWER
        # ---------------------------------------------

        if state == "lower":

            # Add character from v
            alignment_v = v[i - 1] + alignment_v

            # Add gap to w
            alignment_w = "-" + alignment_w

            # Move to the previous state
            state = backtrack_lower[i][j]

            i -= 1

        # ---------------------------------------------
        # UPPER
        # ---------------------------------------------

        elif state == "upper":

            # Add gap to v
            alignment_v = "-" + alignment_v

            # Add character from w
            alignment_w = w[j - 1] + alignment_w

            state = backtrack_upper[i][j]

            j -= 1

        # ---------------------------------------------
        # MIDDLE
        # ---------------------------------------------

        else:

            # Align the two characters
            alignment_v = v[i - 1] + alignment_v
            alignment_w = w[j - 1] + alignment_w

            state = backtrack_middle[i][j]

            i -= 1
            j -= 1

    return best_score, alignment_v, alignment_w

# input

match_reward = 1
mismatch_penalty = 5
gap_opening = 3
gap_extension = 1

v = "AAGTCAACTGTCAACATACGGCAGTGTGCCAACGTACCTCGCTTATGCTTCACGTCAGACTTACTCGGTCAGATATAGGCGCCTCGTCAG"
w = "AATTCAACTGTCAACATACGGCAGTGAGCCAACGTAGCTCGCTTATGTCCCTTTCACGTCAGACTTACTCGGCGGTCAGATATAGGGTAG"

# Solve
score, alignment_v, alignment_w = affine_alignment(
    v,
    w,
    match_reward,
    mismatch_penalty,
    gap_opening,
    gap_extension
)

print(score)
print(alignment_v)
print(alignment_w)