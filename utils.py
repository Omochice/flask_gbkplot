import os
import re

import numpy as np


def window_search(sequence, each=3, overhang=None):
    pretty_sequence = re.findall(r"[atgc]", str(sequence.lower()))

    if overhang == "before":
        for i in range(1, each):
            yield "".join(pretty_sequence[:i])

    for i in range(0, len(pretty_sequence) - each + 1):
        yield "".join(pretty_sequence[i:i + each])

    if overhang == "after":
        for i in range(-1 * each + 1, 0, 1):
            yield "".join(pretty_sequence[i:])


def calculate_coordinates(seq, weight_dict):
    VECTOR_DICT = {"a": [1, 1], "t": [-1, 1], "g": [-1, -1], "c": [1, -1]}
    HOME_DIRECTORY = os.environ["HOME"]
    x_coodinates = [0]
    y_coodinates = [0]

    for triplet in window_search(seq, overhang="before"):
        x_coodinates.append(x_coodinates[-1] + VECTOR_DICT[triplet[-1]][0] *
                            weight_dict.get(triplet, 1))
        y_coodinates.append(y_coodinates[-1] + VECTOR_DICT[triplet[-1]][1] *
                            weight_dict.get(triplet, 1))

    return x_coodinates, y_coodinates
