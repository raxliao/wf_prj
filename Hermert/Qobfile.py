import numpy as np
class Qobfile(object):

    def __init__(self, name):
        self.filename = name
        self.glbfile_name = [ ]
        self.num_file = 0
        self.num_data = 0
        self.num_site = 0

    def get_qobfile_list(self):
        with open(self.filename) as f:
            lines = f.readlines()
            self.num_file = int(lines[0][:-1])
            for index in range(1,self.num_file+1):

                line =lines[index].split()
                self.glbfile_name.append(line[0])

    def load_qobdata(self):
        data_list = []

        for index in range(1,self.num_file+1):

            with open(self.glbfile_name[index-1]) as f:
              #print(self.glbfile_name[index-1])
                line = f.readline()
                while line:
                    num  = list(line.split())
                    data_list.append(num)
                    #print(num)
                    line = f.readline()

        data_array = np.array(data_list)
        self.num_site = data_list.__len__()
        return(data_array)
        #time = data_array[:,0]
        # print(time[0:10])

   # def neu2xyz(self):



            

if __name__ =="__main__":
    filename = "/home/fanw/Work/Reference_Frame/Part2/helmert/datafile.list"
    qobfile = Qobfile("/home/fanw/Work/Reference_Frame/Part2/helmert/datafile.list")
    qobfile.get_qobfile_list()
    print(qobfile.glbfile_name)
