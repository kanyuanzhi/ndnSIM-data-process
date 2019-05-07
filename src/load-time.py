# -*- coding:utf8 -*-

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


def printFormat(filename, value):
    filename_array = filename.split('-')
    strategy_name = filename_array[2]
    zipf = filename_array[3]
    cache_size = filename_array[4]
    request_rate = filename_array[5]
    average_update_time = filename_array[6]
    pit_store_size = filename_array[7]
    update_factor = filename_array[8]
    experiment_time = filename_array[9].split('.')[0]
    print strategy_name + "\t" + request_rate + \
        "\t" + pit_store_size+"\t"+cache_size + "\t" + str(value)
    # print strategy_name + " " + "请求速率: " + request_rate + \
    #     " , PITListStore大小: " + pit_store_size+" , 负载: " + str(value)


if __name__ == "__main__":
    start_index = 41
    # end_index = 340
    end_index = 140
    parameter = 'test'
    file_names = readFileNames(parameter)
    index_array = []
    value_array = []
    average_value = []

    for file_name in file_names:
        name = file_name.split("-")
        lines = readTXT(parameter+"/" + file_name)
        current_index = 1
        index = []
        value = []

        for i in range(1, len(lines)):
            line = lines[i].split("\t")
            if int(line[0]) == current_index and line[1] == "12":
                if "appFace" in line[3] and line[4] == "InData" and line[7] != '0':
                    value.append(float(line[7]))
            elif int(line[0]) != current_index and line[1] == "12":
                index.append(current_index)
                current_index = int(line[0])
        index.append(current_index)
        average_value.append(float(
            sum(value[start_index-1:end_index]))/(end_index-start_index+1))
        # print sum(data_packet_array[start_index-1:end_index])
        index_array.append(index)
        value_array.append(value)

        #print file_name + " : " + str(rate)

    print "名称\t请求速率\tPITListStore大小\t缓存大小\t负载"
    for i in range(len(file_names)):
        printFormat(file_names[i], average_value[i])
        # print value_array[i]
        plt.plot(index_array[i], value_array[i], 'o-', label=file_names[i])
        plt.legend()

    plt.show()
