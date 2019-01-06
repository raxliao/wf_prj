import grep
import re
import numpy as np


def get_org_xyz(filename, time):
    # get delta_xyz forginal point  of time_i form file
    # tow input :1.filename ;
    #            2.time i .
    # one output : xyz

    f = open(filename)
    content = f.read()
    f.close()
    s = "\n".join(re.findall(str(time) + '.*', content))
    # print(s)
    item = re.split("\s+", s)
    xyz = np.multiply(np.array(item[1:4]), [0.001, 0.001, 0.001])  # change unit form mm to m;
    return xyz


if __name__ == "__main__":
    file = '/home/fanw/Work/Reference_Frame/Part2/atmos/geocenter.xyz'
    time = 2010.0014
    xyz = get_org_xyz(file, time)
    print(xyz)
