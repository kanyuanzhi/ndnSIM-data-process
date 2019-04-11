import matplotlib.pyplot as plt
import sys
import os


def readFileName(path, rates):
    names = []
    for name in os.listdir("./" + path):
        # if "normal" not in name:
        if name.split('-')[2] == rates:
            names.append(name)
    return names


def readTXT(txt):
    f = open(txt, "r")
    lines = f.readlines()
    return lines


def readTopology(txt):
    lines = readTXT(txt)
    user_nodes = []
    for line in lines:
        item = line.split(" ")[0]
        if "user" in item:
            user_nodes.append(item)
        if "link" in item:
            return user_nodes


def readRateFile(rate_file_lines):
    current_index = 1
    index_array = []
    interests_packet_array = []
    data_packet_array = []
    interests_packet_rate = 0
    data_packet_rate = 0

    for i in range(1, len(rate_file_lines)):
        line = rate_file_lines[i].split("\t")
        if int(line[0]) == current_index and line[1] == "root":
            if "netDeviceFace" in line[3] and line[4] == "OutData":
                data_packet_rate = data_packet_rate + float(line[7])
        elif int(line[0]) != current_index and line[1] == "root":
            index_array.append(current_index)
            current_index = int(line[0])
            data_packet_array.append(data_packet_rate)
            data_packet_rate = 0

    index_array.append(current_index)
    data_packet_array.append(data_packet_rate)

    return [index_array, data_packet_array]


def getDict(rates):
    start_index = 21
    end_index = 80
    rate_files = readFileName("load-request-rate-change", rates)
    print rate_files
    index_array = []
    rate_array = []
    # line_parameter = ['cx--', 'mo:', 'kp-.', 'r+-']
    average_rate = []
    for rate_file in rate_files:
        result = readRateFile(
            readTXT("./load-request-rate-change/" + rate_file))
        index_array = result[0]
        rate_array.append(result[1])
        average_rate.append(
            float(sum(result[1][start_index-1:end_index]))/(end_index-start_index+1))
        # plt.plot(index_array, result[1], line_parameter[rate_files.index(
        #     rate_file)], label=rate_file)
        # plt.plot(index_array, result[1], label=rate_file)

    dict_index = []
    dict_value = []

    for i in range(0, len(rate_files)):
        dict_index.append(int(rate_files[i].split('-')[4].split('.')[0]))
        dict_value.append(average_rate[i])
    dic = dict(zip(dict_index, dict_value))
    keys = dic.keys()
    keys.sort()
    value_sorted = map(dic.get, keys)
    print keys
    print value_sorted
    return [keys, value_sorted]


if __name__ == "__main__":
    dict_normal = getDict('normal')
    keys_normal = dict_normal[0]
    values_normal = dict_normal[1]

    dict_5 = getDict('5')
    keys_5 = dict_5[0]
    values_5 = dict_5[1]

    dict_10 = getDict('10')
    keys_10 = dict_10[0]
    values_10 = dict_10[1]
    # plt.bar(list(range(len(keys))),value_sorted,tick_label=keys)
    plt.plot(keys_normal, values_normal, 'cx--', label='normal')
    plt.plot(keys_5, values_5, 'kp-.', label='5')
    plt.plot(keys_10, values_10, 'mo:', label='10')
    # plt.plot(index_array, rate_array[0], label=rate_files[0])
    # plt.plot(index_array, rate_array[1], label=rate_files[1])
    # plt.plot(index_array, rate_array[2], label=rate_files[2])
    plt.legend()
    plt.show()
