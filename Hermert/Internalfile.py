import numpy as np
import re


class Internalfile:
    def __init__(self, name):

        self.filename = name
        self.nmode = np.zeros((14, 1))
        self.int_site_num = 0
        self.int_site_name = []

    def read_intfile(self):
        with open(self.filename) as f:

            lines = f.readlines()
            first_line = lines[0]
            second_line = lines[2]

            i = 0
            # print(line)
            flag = 'xyzuvwsXYZUVWS'
            # print(flag[0])

            for i in range(len(first_line)):
                if first_line[i] == flag[i]:
                    self.nmode[i] = 1

            self.int_site_num = int(second_line)
            # print(self.int_site_num)

            for line in lines[3:]:
                #   print(line)

                item = re.split("\s+", line)
                # print(item)
                self.int_site_name.append(item[0])

                # self.int_site_.append(line[1])

    def match_int_site(self, global_site_name, flag_index):
        print('int_site_num', self.int_site_num)
        for i in range(0, self.int_site_num):
            # print(global_site_name[i])
            index = global_site_name.index(self.int_site_name[i])
            flag_index[index] = 1
            # print(i,index)
            # print('len of flag_index= ',flag_index.__len__(),'index',index,'site_name',self.int_site_name[i],'i',i)

        # print('flag index in match sub',flag_index[0:20])


if __name__ == "__main__":
    # filename="/home/fanw/Work/Reference_Frame/Part2/helmert/datafile.list"
    intfile = Internalfile("/home/fanw/Work/Reference_Frame/Part2/helmert/inter.list")
    intfile.read_intfile()
# print(qobfile.glbfile_name)
