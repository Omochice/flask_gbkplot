import glob
import json
import pickle

from Bio import SeqIO

import local_pattern
import utils

if __name__ == "__main__":

    results = []
    gbk_files = glob.glob("static/samples/gbkfiles/*.gbk")

    with open("static/self_information.json", "r") as f:
        weight_dict = json.load(f)

    for gbk_file in gbk_files:
        with open(gbk_file, "r") as f:
            for record in SeqIO.parse(f, "genbank"):
                acc_num = record.name
                x_coo, y_coo = utils.calculate_coordinates(
                    record.seq, weight_dict["default"])
                histgram = local_pattern.make_local_pattern_histgram(
                    x_coo, y_coo)
                results.append((acc_num, tuple(histgram)))

    with open("static/samples/comparisons.pickle", "wb") as f:
        pickle.dump(results, f)
