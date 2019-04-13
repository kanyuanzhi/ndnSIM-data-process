import matplotlib.pyplot as plt
import sys
import os


def readFileName(path):
    names = []
    for name in os.listdir("./" + path):
        if "rate" in name and name.split('-')[0] != "freshness" and name.split('-')[2] != "normal":
            names.append(name)
    return names


def readNormalFileName(path):
    names = []
    for name in os.listdir("./" + path):
        if name.split('-')[2] == "normal":
            names.append(name)
    return names


def readFreshnessFileName(path):
    names = []
    for name in os.listdir("./" + path):
        if "rate" in name and name.split('-')[0] == "freshness":
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
            if "appFace" in line[3] and line[4] == "InData":
                data_packet_array.append(float(line[7]))
        elif int(line[0]) != current_index and line[1] == "root":
            index_array.append(current_index)
            current_index = int(line[0])
    index_array.append(current_index)



    #     if int(line[0]) == current_index and line[1] == "root":
    #         if "netDeviceFace" in line[3] and line[4] == "OutData":
    #             data_packet_rate = data_packet_rate + float(line[7])
    #     elif int(line[0]) != current_index and line[1] == "root":
    #         index_array.append(current_index)
    #         current_index = int(line[0])
    #         data_packet_array.append(data_packet_rate)
    #         data_packet_rate = 0

    # index_array.append(current_index)
    # data_packet_array.append(data_packet_rate)

    return [index_array, data_packet_array]


def getDict(flag):
    start_index = 21
    end_index = 80
    if flag == "kan":
        rate_files = readFileName("load-publish-rate-change")
    if flag == "freshness":
        rate_files = readFreshnessFileName("load-publish-rate-change")
    if flag == "normal":
        rate_files = readNormalFileName("load-publish-rate-change")
    index_array = []
    rate_array = []
    # line_parameter = ['cx--', 'mo:', 'kp-.', 'r+-']
    average_rate = []
    for rate_file in rate_files:
        result = readRateFile(
            readTXT("./load-publish-rate-change/" + rate_file))
        index_array = result[0]
        rate_array.append(result[1])
        average_rate.append(
            float(sum(result[1][start_index-1:end_index]))/(end_index-start_index+1))

    dict_index = []
    dict_value = []

    if flag == "normal":
        return [0, average_rate]
    else:
        for i in range(0, len(rate_files)):
            if flag == "freshness":
                dict_index.append(float(rate_files[i].split('-')[3]))
            else:
                dict_index.append(float(rate_files[i].split('-')[2]))
            dict_value.append(average_rate[i])
        dic = dict(zip(dict_index, dict_value))
        keys = dic.keys()
        keys.sort()
        value_sorted = map(dic.get, keys)
        print value_sorted

        return [keys, value_sorted]


if __name__ == "__main__":
    

    dict_kan = getDict("kan")
    keys_kan = dict_kan[0]
    values_kan = dict_kan[1]

    dict_freshness = getDict("freshness")
    keys_freshness = dict_freshness[0]
    values_freshness = dict_freshness[1]

    dict_normal = getDict("normal")
    keys_normal = keys_kan[:]
    values_normal = dict_normal[1]*len(keys_normal)
    

    # plt.bar(list(range(len(keys))),value_sorted,tick_label=keys)
    plt.plot(keys_kan, values_kan, 'cx--', label='kan')
    plt.plot(keys_freshness, values_freshness, 'kp-.', label='freshness')
    plt.plot(keys_normal, values_normal, 'mo:', label='normal')
    # plt.plot(index_array, rate_array[0], label=rate_files[0])
    # plt.plot(index_array, rate_array[1], label=rate_files[1])
    # plt.plot(index_array, rate_array[2], label=rate_files[2])
    plt.legend()
    plt.show()
