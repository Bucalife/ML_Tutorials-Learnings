###########################
# 6.0002 Problem Set 1b: Space Change
# Name:
# Collaborators:
# Time:
# Author: charz, cdenise

#================================
# Part B: Golden Eggs
#================================

# Problem 1
def dp_make_weight(egg_weights, target_weight, memo={}):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.
    
    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)
    
    Returns: int, smallest number of eggs needed to make target weight
    """
    min_taken = float('inf')    # define an impossible value

    if target_weight == 0:      # When I can't transport nothing I return just 0
        return 0

    elif target_weight in memo:     # if the weight I can transport is memorized I return the item I memorized
        return memo[target_weight]

    elif target_weight > 0:     # SO... if I actually have a weight to fill
        for weight in egg_weights:  # I check the possible weights I can choose from
            # We open X virtual universes with a new target weight for each of possible weight eggs.
            # Each universe will consider a different target weight
            sub_result = dp_make_weight(egg_weights, target_weight - weight)
            print(sub_result)
            # I choose the minimum value between my N universe result and inf
            min_taken = min(min_taken, sub_result)
            print(f'--- {min_taken} ---')
            print(memo)

    memo[target_weight] = min_taken + 1     # I add to my memo dict the minimum I have identified
    return min_taken + 1    # Return something impossible if


    # Greedy Solution
    # egg_weights_lst = sorted([i for i in egg_weights], reverse=True)
    # for i in range(len(egg_weights_lst)):
    #     memo[egg_weights_lst[i]] = target_weight // egg_weights_lst[i]
    #     target_weight = target_weight % egg_weights_lst[i]
    # #print(memo)
    # return sum(memo.values())


# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = (1, 6, 9)
    n = 14
    print("Egg weights = (1, 5, 10, 25)")
    print("n = 99")
    print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()