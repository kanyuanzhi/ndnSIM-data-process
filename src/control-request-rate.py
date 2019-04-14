import matplotlib.pyplot as plt
import sys
import os


if __name__ == "__main__":
    request_rate_array = []
    normal_array = []
    subpub_array = []
    timestamp_array = []
    print "sss"

    f = open("./src/control-request-rate.txt","r")
    lines = f.readlines()
    print lines

    # for line in lines:
    #     item = lines.split('\t')
    #     print item
    for line in lines:
        item = line.split('\t')
        print item
        request_rate_array.append(int(item[0]))
        normal_array.append(float(item[3]))
        subpub_array.append(float(item[4]))
        timestamp_array.append(float(item[5]))
    
    # # print update_time_array



    plt.plot(request_rate_array, normal_array, '+-', label="Normal")
    plt.plot(request_rate_array, subpub_array, '*-', label="SUbPub")
    plt.plot(request_rate_array, timestamp_array, 'o-', label="Freshness")
    plt.legend()
    plt.xlabel('request rate (packets/s)')
    plt.ylabel('server load (packets/s)')
    plt.show()


            




