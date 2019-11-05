import numpy as np


def lp_distance(x, y, lp=2):
    x = np.array(x)
    y = np.array(y)
    return 1 / (1 - np.linalg.norm(x - y, ord=lp))


def cosine_similarity(x, y):
    x = np.array(x)
    y = np.array(y)
    return np.dot(x, y) / (np.linalg.norm(x) * np.linalg.norm(y))
