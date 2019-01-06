import numpy as np

from const import const


class Aprfile(object):

    def __init__(self, name):
        self.filename = name
        self.site_apr = []
        self.site_num = 0
        self.xyz_ti = []
        self.site_name = []

    def read_apr_file(self):
        # QOCA apr format
        with open(self.filename) as f:

            line = f.readline()
            while line:
                num = list(line.split())
                if (num.__len__() >= 16):
                    num[5] = " ".join([num[5], num[6]])
                    num.remove(num[6])

                temp = []
                temp.append(num[0])  # site_name
                if (num[2][0] == 'N'):
                    B = int(num[2][1:3]) + float(num[3]) / 60 + float(num[4]) / 3600
                else:
                    B = -1 * (int(num[2][1:3]) + float(num[3]) / 60 + float(num[4]) / 3600)

                temp.append(B)  # Latitude
                if (num[5][0] == 'E'):
                    L = int(num[5][1:4]) + float(num[6]) / 60.0 + float(num[7]) / 3600
                else:
                    L = -1 * (int(num[5][1:4]) + float(num[6]) / 60 + float(num[7]) / 3600)
                temp.append(L)  # longtitude
                temp.append(float(num[8]))  # height

                temp.append(float(num[9]))  # velocity_U
                temp.append(float(num[10]))  # velocity_V
                temp.append(float(num[11]))  # velocity_W
                temp.append(float(num[12]))  # time0

                self.site_name.append(num[0])
                self.site_apr.append(temp)
                self.site_num = self.site_num + 1

                line = f.readline()

    # print(self.site_apr)

    def gen_xyz(self,ti):
        for i in range(0, self.site_num):
            xyz_temp = self.blh_neu_2xyz(self.site_apr[i][1:4], self.site_apr[i][4:7], ti, self.site_apr[i][7])
            self.xyz_ti.append(xyz_temp)

    def blh_neu_2xyz(self, blh, uvw, ti, t0):
        #   ti=t0
        #   d_neu=np.array(uvw)*(ti-t0)

        xyz0 = self.blh2xyz(np.array(blh))
        #    xyz=self.d_neu2xyz(d_neu.transpose(),np.array(blh),xyz0)
        return np.array(xyz0)

    def blh2xyz(self, blh):
        con = const()
        B = blh[0] / 180.0 * con.pi
        L = blh[1] / 180.0 * con.pi
        H = blh[2]

        N = con.a / (np.sqrt(1 - con.e * con.e * np.sin(B)))
        xyz = np.zeros((3, 1))
        xyz[0] = (N + H) * np.cos(B) * np.cos(L)
        xyz[1] = (N + H) * np.cos(B) * np.sin(L)
        xyz[2] = (N * (1 - con.e * con.e) + H) * np.sin(B)
        return xyz

    def d_neu2xyz(self, neu, blh, xyz0):
        M = np.zeros((3, 3))

        con = const()
        B = blh[0] / 180.0 * con.pi
        L = blh[1] / 180.0 * con.pi
        H = blh[2]

        M[0, 0] = -1 * np.sin(L)
        M[0, 1] = np.cos(L)
        M[0, 2] = 0
        M[1, 0] = -1 * np.sin(B) * np.cos(L)
        M[1, 1] = -1 * np.sin(B) * np.sin(L)
        M[1, 2] = np.cos(B)
        M[2, 0] = np.cos(B) * np.cos(L)
        M[2, 1] = np.cos(B) * np.sin(L)
        M[2, 2] = np.sin(B)

        M1 = np.linalg.inv(M)
        xyz = np.zeros((3, 1))
        neu = neu.astype(float)
        xyz = M1.dot(neu) + xyz0
        return xyz

    def xyz2neu(self, xyz, blh, xyz0):
        M = np.zeros((3, 3))

        con = const()
        B = blh[0] / 180.0 * con.pi
        L = blh[1] / 180.0 * con.pi
        H = blh[2]

        M[0, 0] = -1 * np.sin(L)
        M[0, 1] = np.cos(L)
        M[0, 2] = 0
        M[1, 0] = -1 * np.sin(B) * np.cos(L)
        M[1, 1] = -1 * np.sin(B) * np.sin(L)
        M[1, 2] = np.cos(B)
        M[2, 0] = np.cos(B) * np.cos(L)
        M[2, 1] = np.cos(B) * np.sin(L)
        M[2, 2] = np.sin(B)

        neu = np.zeros((3, 1))
        # neu=neu.astype(float)
        neu = M.dot(xyz - xyz0)
        return neu

    def check_site(self, site_list, flag):
        flag = 'true'
        for site in site_list:
            if (site not in self.site_apr):
                flag = 'false'
                print('site ', site, 'not in aprfile', self.filename)

    def get_index_site(self, site):
        index = self.site_name.index(site)
        return index

    def get_site_xyz(self, site, time):
        i = self.get_index_site(site)
        xyz_temp = self.blh_neu_2xyz(self.site_apr[i][1:4], self.site_apr[i][4:7], time, self.site_apr[i][7])
        return xyz_temp


if __name__ == "__main__":
    # neu = np.array([[0],[0],[100]])
    # xyz = np.array([[0],[0],[0]])
    # aprfile=Aprfile('ttt')
    # aprfile.blh2xyz(neu,xyz)
    # aprfile.d_neu2xyz(neu,xyz,xyz)
    # print(xyz)

    aprfile = Aprfile("/home/fanw/Work/Reference_Frame/Part2/helmert/site.net")
    aprfile.read_apr_file()
    # print(aprfile.site_apr[1][:])
    # print(aprfile.site_num)
    index = aprfile.get_index_site('0009_GPS')
    print(index)
