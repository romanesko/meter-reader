import random


def generate_random_numbers(X, A, B, ratios):
    # Calculate the number of intervals based on the length of the ratios list
    num_intervals = len(ratios)

    # Calculate the size of each interval
    interval_size = (B - A) / num_intervals

    # Initialize the result list
    result = []

    # Generate X random numbers
    for _ in range(X):
        # Select a random interval index based on the ratios
        interval_index = random.choices(range(num_intervals), weights=ratios)[0]

        # Calculate the lower and upper bounds of the selected interval
        interval_lower = A + interval_index * interval_size
        interval_upper = interval_lower + interval_size

        # Generate a random number within the selected interval
        random_number = random.uniform(interval_lower, interval_upper)

        # Add the random number to the result list
        result.append(int(random_number))

    return result
