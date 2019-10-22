import re


def window_search(sequence):
    pretty_sequence = re.findall(r"[atgc]", sequence.lower())
    for i in range(1, len(pretty_sequence) + 1):
        if i < 3:
            yield "".join(pretty_sequence[:i])
        else:
            yield "".join(pretty_sequence[i - 3:i])
