# Problem Set 4A
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''

    # Needed to stop the recursion
    if len(sequence) <= 1:
        print('I am back to the Original universe, I proceed in the loop')
        return [sequence]

    else:
        result = []     # Need a list of permutations to return as a final result
        for perm in get_permutations(sequence[1:]):     # Create different universes per call
            for i in range(len(sequence)):      # for each universe I start back to the top and consider 0, 1, 2 ... len
                # All result from 2 universe are added bu erased in the first universe from which I get the result
                result.append(perm[:i] + sequence[0:1] + perm[i:])

    return result


if __name__ == '__main__':
   #EXAMPLE
   example_input = 'abc'
   print('Input:', example_input)
   print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
   print('Actual Output:', get_permutations(example_input))

   example_input = '123'
   print('Input:', example_input)
   print('Expected Output:', ['123', '132', '213', '231', '312', '321'])
   print('Actual Output:', get_permutations(example_input))
    
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)


