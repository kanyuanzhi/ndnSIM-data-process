import matplotlib.pyplot as plt
import sys
import os


if __name__ == "__main__":
    update_time_array = []
    pitcs_size_array = []
    load_array = []

    update_time = 0
    pitcs_size = []
    load = []
    f = open("./src/data.txt","r")
    lines = f.readlines()
    for line in lines:
        item = line.split('\t')
        if float(item[0]) in update_time_array:
            pitcs_size.append(int(item[1]))
            load.append(float(item[2]))
            update_time = float(item[0])
        else:
            update_time_array.append(float(item[0]))
            if len(pitcs_size) != 0:
                pitcs_size_array.append(pitcs_size)
                load_array.append(load)
                pitcs_size = []
                load = []
    pitcs_size_array.append(pitcs_size)
    load_array.append(load)

    print update_time_array
    print pitcs_size_array[0]
    print load_array[0]


    for i in range(len(load_array)):
        plt.subplot(3, 3, i+1)
        plt.plot(pitcs_size_array[i], load_array[i], '+-', label=str(update_time_array[i]) + ' s')
        plt.legend()
        plt.xlabel('PITList Content Store Size (packets)')
        plt.ylabel('server load (packets/s)')
       
    plt.show()


            




