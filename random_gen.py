import functools
from numpy import random


# def create_probability_map(trait_nums, trait_probs):
#     if (len(trait_nums) == len(trait_probs)) and (sum(trait_probs) == 100):
#
#         cumulatives = [sum(trait_probs[0:x:1]) for x in range(0, len(trait_probs) + 1)]
#         return cumulatives[1:]
#     else:
#         print("Input array lengths not equal or probabilities are not equal to 100")


def get_random_index(trait_prob_map):

    # generate random number
    random_num = random.randint(1, trait_prob_map[-1])

    for index, bound in enumerate(trait_prob_map):
        if random_num <= bound:
            return index
        else:
            continue
