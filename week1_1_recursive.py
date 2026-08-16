def recursive_change(money, coins):
    if money == 0:
        return 0

    min_num_coins = float("inf")

    for coin in coins:
        if money >= coin:
            num_coins = recursive_change(money - coin, coins)

            if num_coins + 1 < min_num_coins:
                min_num_coins = num_coins + 1

    return min_num_coins

money = 76
coins = [5, 4, 1]
print(recursive_change(money, coins))

### TOOOOO SLOWWWW 
