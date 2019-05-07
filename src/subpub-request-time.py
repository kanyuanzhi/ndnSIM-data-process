import matplotlib.pyplot as plt
import sys
import os


if __name__ == "__main__":
    request_rate_array = []
    pitcs_size_array = []
    load_array = []

    request_rate = 0
    pitcs_size = []
    load = []
    f = open("./src/subpub-request-time.txt","r")
    lines = f.readlines()
    for line in lines:
        item = line.split('\t')
        request_rate = float(item[0])
        if request_rate in request_rate_array:
            pitcs_size.append(int(item[2]))
            load.append(float(item[5]))
        else:
            request_rate_array.append(request_rate)
            if len(pitcs_size) == 0:
                pitcs_size.append(int(item[2]))
                load.append(float(item[5]))
            else:
                pitcs_size_array.append(pitcs_size)
                load_array.append(load)
                print len(pitcs_size)
                print len(load)
                pitcs_size = [int(item[2])]
                load = [float(item[5])]

                
    print len(pitcs_size)
    print len(load)
    pitcs_size_array.append(pitcs_size)
    load_array.append(load)

    print request_rate_array
    print pitcs_size_array[0]
    print load_array[0]


    for i in range(len(load_array)):
        plt.subplot(3, 3, i+1)
        plt.plot(pitcs_size_array[i], load_array[i], '+-', label=str(request_rate_array[i]) + ' s')
        plt.legend()
        plt.xlabel('PITList Content Store Size (packets)')
        plt.ylabel('server load (packets/s)')
       
    plt.show()


            




