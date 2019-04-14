import matplotlib.pyplot as plt
import sys
import os


if __name__ == "__main__":
    update_time_array = []
    normal_array = []
    subpub_array = []
    timestamp_array = []
    print "sss"

    f = open("./src/control-update-time.txt","r")
    lines = f.readlines()
    print lines

    # for line in lines:
    #     item = lines.split('\t')
    #     print item
    for line in lines:
        item = line.split('\t')
        print item
        update_time_array.append(float(item[0]))
        normal_array.append(float(item[2]))
        subpub_array.append(float(item[3]))
        timestamp_array.append(float(item[4]))
    
    # # print update_time_array



    plt.plot(update_time_array, normal_array, '+-', label="Normal")
    plt.plot(update_time_array, subpub_array, '*-', label="SUbPub")
    plt.plot(update_time_array, timestamp_array, 'o-', label="Freshness")
    plt.legend()
    plt.xlabel('update time (s)')
    plt.ylabel('server load (packets/s)')
    plt.show()


            




