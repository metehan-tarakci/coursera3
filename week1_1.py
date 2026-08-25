"""To solve m:

1. Try every coin.
2. Pretend we use that coin.
3. Look at the answer we already calculated for m - coin.
4. Add 1 for the coin we just used.
5. Keep the smallest answer."""

def dp_change(money, coins):
    # Create a list to store the minimum number of coins
    # needed to make every amount from 0 up to 'money'
    # min_num_coins[0] = minimum coins needed to make 0
    #min_num_coins[1] = minimum coins needed to make 1
    #min_num_coins[2] = minimum coins needed to make 2 ...
    #min_num_coins[6] = minimum coins needed to make 6
    min_num_coins = [0] * (money + 1)
    backtrack = [str(0)] * (money + 1)


    # Solve the problem for each amount from 1 to 'money'
    for m in range(1, money + 1):

        # Start by assuming the answer is infinity
        # We will replace this with a smaller value
        # when we find a possible combination of coins
        min_num_coins[m] = float("inf")

        # Try every available coin
        for coin in coins:

            # We can only use the coin if it is not
            # larger than the current amount
            if m >= coin:

                # Check whether using this coin gives us
                # a better solution than the best one found so far
                #
                # m - coin = the remaining amount after using the coin
                # min_num_coins[m - coin] = minimum coins needed
                #                               for that remaining amount
                # + 1 = the coin we are using right now
                if min_num_coins[m - coin] + 1 < min_num_coins[m]:

                    # If this is a better solution, save it
                    # as the new minimum number of coins for m
                    min_num_coins[m] = min_num_coins[m - coin] + 1
                    backtrack[m] = str(coin) + " " + backtrack[m-coin]

    # Return the minimum number of coins needed to make 'money'
    return min_num_coins[money], str(backtrack[money])

coins = [1, 4, 5]
money = 11

min_num_coins, list_of_coins = dp_change(money, coins)
print(min_num_coins)
print(list_of_coins[:-1])

