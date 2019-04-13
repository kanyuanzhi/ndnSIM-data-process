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
    parameters = ["request-rate", "update-time", "cache-size", "zipf"]
    name_id = [5, 6, 4, 3]
    flag = 1
    file_names = readFileNames(parameters[flag])
    normal_index = []
    normal_rate = []
    subpub_index = []
    subpub_rate = []
    timestamp_index = []
    timestamp_rate = []
    load_array = []
    for file_name in file_names:
        name = file_name.split("-")
        lines = readTXT(parameters[flag]+"/" + file_name)
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
        if name[2] == "Normal":
            normal_index.append(round(float(name[name_id[flag]]), 1))
            normal_rate.append(rate)
        elif name[2] == "SubPub":
            subpub_index.append(round(float(name[name_id[flag]]), 1))
            subpub_rate.append(rate)
        elif name[2] == "Timestamp":
            timestamp_index.append(round(float(name[name_id[flag]]), 1))
            timestamp_rate.append(rate)
        print file_name + " : " + str(rate)
        # plt.plot(index_array[20:40], data_packet_array[20:40], label=file_name)
        # plt.plot(index_array, data_packet_array, label=file_name)
    (normal_index, normal_rate) = sortData(normal_index, normal_rate)
    (subpub_index, subpub_rate) = sortData(subpub_index, subpub_rate)
    (timestamp_index, timestamp_rate) = sortData(
        timestamp_index, timestamp_rate)

    # for i in range(len(file_names)):
    #     print file_names[i]
    #     print load_array[i]
    plt.plot(normal_index, normal_rate, 'cx--', label="Normal")
    plt.plot(subpub_index, subpub_rate, 'mo:', label="SubPub")
    plt.plot(timestamp_index, timestamp_rate, 'kp-.', label="Timestamp")
    plt.legend()
    plt.show()
