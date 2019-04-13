import matplotlib.pyplot as plt
import sys
import os


def readFileNames(path):
    names = []
    for name in os.listdir("./rate-data/" + path):
        if "rate" in name:
            names.append(name)
    return names


def readTXT(txt):
    f = open("./rate-data/"+txt, "r")
    lines = f.readlines()
    return lines


def sortData(index, rate):
    dic = dict(zip(index, rate))
    keys = dic.keys()
    keys.sort()
    rate_sorted = map(dic.get, keys)
    return (keys, rate_sorted)


if __name__ == "__main__":
    start_index = 21
    end_index = 80
    parameter = 'pitcs-size'
    file_names = readFileNames(parameter)
    normal_index = []
    normal_rate = []
    subpub_index = []
    subpub_rate = []

    load_array = []
    for file_name in file_names:
        name = file_name.split("-")
        lines = readTXT(parameter+"/" + file_name)
        current_index = 1
        index_array = []
        data_packet_array = []
        for i in range(1, len(lines)):
            line = lines[i].split("\t")
            if int(line[0]) == current_index and line[1] == "12":
                if "appFace" in line[3] and line[4] == "InData":
                    data_packet_array.append(float(line[7]))
            elif int(line[0]) != current_index and line[1] == "12":
                index_array.append(current_index)
                current_index = int(line[0])
        index_array.append(current_index)
        rate = float(
            sum(data_packet_array[start_index-1:end_index]))/(end_index-start_index+1)
        subpub_index.append(round(float(name[7].split('.')[0]), 1))
        subpub_rate.append(rate)

        print file_name + " : " + str(rate)

    (subpub_index, subpub_rate) = sortData(subpub_index, subpub_rate)


    # for i in range(len(file_names)):
    #     print file_names[i]
    #     print load_array[i]
    plt.plot(subpub_index, subpub_rate, 'mo:', label="SubPub")
    plt.legend()
    plt.show()
