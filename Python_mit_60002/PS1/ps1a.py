###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time


# ================================
# Part A: Transporting Space Cows
# ================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    herd_cows = {}
    with open(filename, 'r') as cows:
        for line in cows:
            cow_str = line.split(',')
            herd_cows[cow_str[0]] = cow_str[1].strip('\n')

    return herd_cows


# Problem 2
def greedy_cow_transport(cows: dict, limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    sorted_cows = list(sorted(cows.items(), key=lambda item: item[1], reverse=True))
    trips = []

    def single_trip(sorted_cows_list):
        # Each Trip is defined by the greedy algorithm
        trip_weight = 0
        this_trip = []
        for i in range(len(sorted_cows_list)):
            if (trip_weight + int(sorted_cows_list[i][1])) <= limit:
                this_trip.append(sorted_cows_list[i][0])
                trip_weight += int(sorted_cows_list[i][1])
        return this_trip

    # As far as we have cows we continue to choose from the one that are avaliable
    while len(sorted_cows) != 0:
        trip = single_trip(sorted_cows)
        trips.append(trip)
        sorted_cows = [i for i in sorted_cows if i[0] not in trip]

    return trips


# Problem 3
def brute_force_cow_transport(cows, limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """

    # Create a list of all the possible trips based on our constrain (limit)
    cows_name = [i for i in cows.keys()]
    valid_trips = []

    for possible_trips in get_partitions(cows_name):
        transportable = 0

        for trip in possible_trips:
            trip_weight = [int(cows[cow]) for cow in trip]

            if sum(trip_weight) <= limit:
                transportable += 1

            if transportable == len(possible_trips):
                valid_trips.append(possible_trips)

    # Find optimal list out of the possibilities
    len_trip = [len(trip) for trip in valid_trips]
    optimal_trip = len_trip.index(min(len_trip))

    return valid_trips[optimal_trip]


# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    start = time.time()
    print(brute_force_cow_transport(cows))
    end = time.time()
    print(f'The brute force algorithm take {end - start}')

    start = time.time()
    print(greedy_cow_transport(cows))
    end = time.time()
    print(f'The brute force algorithm take {end - start}')


if __name__ == '__main__':
    cows = load_cows('ps1_cow_data.txt')
    print(cows)
    compare_cow_transport_algorithms()