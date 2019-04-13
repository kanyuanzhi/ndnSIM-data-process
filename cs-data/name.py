import os

path = os.getcwd()
names = os.listdir(path)

for oldname in names:
    if 'cs' in oldname:
        temp = oldname.split('-')
        update_time = temp[2]
        pitcs_size = temp[3].split('.')[0]
        newname = 'cs-trace-SubPub-1.2-100-100-'+update_time+'-'+pitcs_size+'.txt'
        os.rename(os.path.join(path,oldname),os.path.join(path,newname))
        print path+'/'+oldname
        print path+'/'+newname
