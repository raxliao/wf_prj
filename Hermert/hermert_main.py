#!/usr/bin/python
import os
import numpy as np
from numpy.linalg import inv
from Qobfile import Qobfile
from drvfile import drvfile
from Internalfile import Internalfile
from Aprfile import Aprfile
from generate_design_matrix import generate_design_matrix
import get_org_xyz

#def hermert_main(drv_file_name,workdir):
#def hermert_main ( ):
# Hermert transformat code
# 1: Read data and Setup
# 2: Creat array
# 3: Calculate
# 4: Cal rms
# 5: Output
#print("hello")
# 1.1 Read data:
#from read_drvfile import read_drvfile


glb_filename = ['','']
drv_file_name = '/home/fanw/Work/Reference_Frame/Part2/helmert/st_filter.drv'
workdir = '/home/fanw/Work/Reference_Frame/Part2/helmert/'
os.chdir(workdir)
drv_file = drvfile(drv_file_name)
drv_file.read_drvfile()


# 1.2 Read apr
print('Read apr file :')
apr_file = Aprfile(drv_file.apr_filename)
apr_file.read_apr_file()
#apr_file.gen_xyz(time)



# 1.3 get qob file list, stored in global index list
# data are stored in data_array matrix
# neu should be converted  to xyz for later calculation
print('get qob file list')
qob_file = Qobfile(drv_file.in_listname)
qob_file.get_qobfile_list()
data_array=qob_file.load_qobdata()

site_name = list(data_array[:,10])
flag_index = np.zeros((qob_file.num_site,1))
d_neu = data_array[:,(1,2,6)]**[0.001,0.001,0.001]
xyz_CE = np.zeros((qob_file.num_site,3))
xyz_CM = np.zeros((qob_file.num_site,3))
xyz_apr = np.zeros((qob_file.num_site,3))
time = data_array[0,0]
org_xyz = get_org_xyz(drv_file.geocenter_filename,time)
# .1 convert observation neu to xyz
# .2 get apr file coordinate file
# loop by site
for i in range (0,qob_file.num_site):

    neu = np.array(d_neu[i,:])
    neut = np.zeros((3,1))
    for j in range (0,3):
        neut[j,0] = neu[j]
    # get site BLH from aprfile ,first should get the index of site i
    index_temp = apr_file.get_index_site(site_name[i])
    blh = apr_file.site_apr[index_temp][1:4]
    xyz0 = apr_file.blh2xyz(np.array(blh))
    xyz_temp=apr_file.d_neu2xyz(neut, np.array(blh), xyz0)
    xyz_CE[i,:] = xyz_temp.transpose()

    # get apr
    xyz_temp = apr_file.get_site_xyz(site_name[i],time)
    xyz_apr[i,:] =  xyz_temp.transpose()

xyz_CM=xyz_CE+org_xyz
# 1.4 get internal constraint list
print('get internal constraint list')
int_file = Internalfile(drv_file.internal_consname)
int_file.read_intfile()
int_file.match_int_site(site_name,flag_index)
xyz_frame = np.zeros((int_file.int_site_num,3))
for i in range (0,int_file.int_site_num):
    xyz_temp = apr_file.get_site_xyz(int_file.int_site_name[i],time)

    xyz_frame[i,:] =  xyz_temp.transpose()

# 2 Generate design matrix A 3*n,7  and L
# A
A = np.zeros((3*int_file.int_site_num,7))
L = np.zeros((3 * int_file.int_site_num, 1))
index_int_site = []
for i in range (0,qob_file.num_site):
    if (flag_index[i]==1):
        index_int_site.append(i)


for i in range (0,int_file.int_site_num):


    x1 = xyz[index_int_site[i],0]
    y1 = xyz[index_int_site[i],1]
    z1 = xyz[index_int_site[i],2]

    x2 = xyz_frame[i,0]
    y2 = xyz_frame[i,1]
    z2 = xyz_frame[i,2]

    A_temp = generate_design_matrix(x1,y1,z1)

    A[3*i:3*i+3,:] = A_temp


    L[3*i,0] = x2-x1
    L[3*i+1, 0] = y2 - y1
    L[3*i+2, 0] = z2 - z1

#3. Calculate transform parameter:
At = A.T
Naa = inv(At.dot(A))
T = (Naa.dot(At)).dot(L)

#4. Calculate transformed coordinates :
obs_temp = np.zeros((3,1))
#A_temp = np.zeros((3,7))

Transformed_XYZ = np.zeros((3*qob_file.num_site,3))
for i in range(0,qob_file.num_site):
    x1 = xyz[i, 0]
    y1 = xyz[i, 1]
    z1 = xyz[i, 2]
    obs_temp = np.array([[x1],[y1],[z1]])
    A_temp =  generate_design_matrix(x1,y1,z1)
    cal_temp = obs_temp + A_temp.dot(T)
    Transformed_XYZ[i,:] = cal_temp.T

#5. Out put
#two part need to be ouput:
#5.1 Transform parameter

f = open(drv_file.transform_parameter_file,'a+')
for i in range (0,7):
 f.write("%16.4f  " %(T[i]))

f.write("  \n")
f.close()
print(T)
#5.2 Transformed coordinates of each site

f = open(drv_file.out_filename,'w')
for i in range (0,qob_file.num_site):

    f.write(" %9s  %15.4f  %15.4f  %15.4f  %15.4f  %15.4f  %15.4f " %(site_name[i],xyz[i,0],xyz[i,1],xyz[i,2],Transformed_XYZ[i,0],Transformed_XYZ[i,1],Transformed_XYZ[i,2]))
    f.write(" %6.2f  %6.2f  %6.2f  %f \n"%(Transformed_XYZ[i,0]-xyz_apr[i,0],Transformed_XYZ[i,1]-xyz_apr[i,1],Transformed_XYZ[i,2]-xyz_apr[i,2],flag_index[i]))

f.close()

f = open(drv_file.res_filename,'w')
for i in range (0,qob_file.num_site):
    blh = apr_file.site_apr[i][1:4]
    blh_temp=np.array([[blh[0]],[blh[1]],[blh[2]]])
    xyz33_temp=np.array([[Transformed_XYZ[i,0]],[Transformed_XYZ[i,1]],[Transformed_XYZ[i,2]]])
    xyz00_temp=np.array([[xyz_apr[i,0]],[xyz_apr[i,1]],[xyz_apr[i,2]]])

    neu_temp=apr_file.xyz2neu(xyz33_temp,blh_temp,xyz00_temp)
    f.write("%9s  %10.4f  %10.4f %10.4f \n"%(site_name[i],neu_temp[0],neu_temp[1],neu_temp[2]))

f.close()