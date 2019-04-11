import matplotlib.pyplot as plt
import sys
import os


def readFileName(path):
    names = []
    for name in os.listdir("./" + path):
        if "rate" in name:
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
    interests_packet_rate = 0.0
    data_packet_rate = 0.0

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


if __name__ == "__main__":
    start_index = 21
    end_index = 180
    rate_files = readFileName("rate")
    index_array = []
    rate_array = []
    line_parameter = ['cx--', 'mo:', 'kp-.', 'r+-']
    average_rate = []
    for rate_file in rate_files:
        result = readRateFile(readTXT("./rate/" + rate_file))
        index_array = result[0]
        rate_array.append(result[1])
        average_rate.append(
            float(sum(result[1][start_index-1:end_index]))/(end_index-start_index+1))
        # plt.plot(index_array, result[1], line_parameter[rate_files.index(
        #     rate_file)], label=rate_file)
        # plt.plot(index_array, result[1], label=rate_file)
    print rate_files
    print average_rate

    dict_index = []
    dict_value = []
    
    for i in range(0, len(rate_files)):
        if rate_files[i].split('-')[2] == "normal":
            dict_index.append(0)
        else:
            dict_index.append(int(rate_files[i].split('-')[2]))
        dict_value.append(average_rate[i])
    dic = dict(zip(dict_index, dict_value))
    print dic
    keys = dic.keys()
    keys.sort()
    value_sorted = map(dic.get, keys)
    plt.bar(list(range(len(keys))),value_sorted,tick_label=keys)
    # plt.plot(index_array, rate_array[0], label=rate_files[0])
    # plt.plot(index_array, rate_array[1], label=rate_files[1])
    # plt.plot(index_array, rate_array[2], label=rate_files[2])
    #plt.legend()
    #plt.show()
